from typing import Any, Final

from exceptions import NotFoundException
from restaurants.dtos import CreateRestaurantDto, SearchRestaurantsDto
from restaurants.handlers import RestaurantExceptionHandler
from restaurants.models import IPAddress, Restaurant, RestaurantImage, Review
from restaurants.validators import RestaurantValidator
from utils.clients import NaverClient
from utils.parsers import remove_html_tags


class RestaurantService:
    DAEGU_PREFIX: Final[str] = "대구광역시"
    GYUNGSAN_PREFIX: Final[str] = "경상북도 경산시"
    METERS_PER_KM: Final[int] = 1000

    def __init__(self):
        self._naver_client: NaverClient = NaverClient()
        self._validator: RestaurantValidator = RestaurantValidator()
        self._exception_handler: RestaurantExceptionHandler = (
            RestaurantExceptionHandler()
        )

    def _filter_daegu_gyungsan_restaurants(
        self, restaurants: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        return [
            restaurant
            for restaurant in restaurants
            if restaurant.get("roadAddress", "").startswith(self.DAEGU_PREFIX)
            or restaurant.get("roadAddress", "").startswith(self.GYUNGSAN_PREFIX)
        ]

    def _clean_road_address(self, name: str, road_address: str) -> str:
        return (
            road_address[: -len(name)].strip()
            if road_address.endswith(name)
            else road_address
        )

    def _create_search_dto(self, restaurant: dict[str, Any]) -> SearchRestaurantsDto:
        name = remove_html_tags(restaurant.get("title", ""))
        road_address = self._clean_road_address(name, restaurant.get("roadAddress", ""))
        return SearchRestaurantsDto(name=name, road_address=road_address)

    def search_restaurants(self, name: str) -> list[SearchRestaurantsDto]:
        try:
            restaurants: list[dict[str, Any]] = self._naver_client.search_places(
                name=name
            )
        except Exception as exc:
            raise self._exception_handler.handle_search_exceptions(exc)

        daegu_restaurants: list[dict[str, Any]] = (
            self._filter_daegu_gyungsan_restaurants(restaurants)
        )
        search_results: list[SearchRestaurantsDto] = [
            self._create_search_dto(restaurant) for restaurant in daegu_restaurants
        ]

        if not search_results:
            raise NotFoundException("해당하는 식당이 없습니다.")

        return search_results

    def _get_geocode_data(self, address: str) -> tuple[str, str, float]:
        try:
            return self._naver_client.get_geocode_distance_by_address(address=address)
        except Exception as exc:
            raise self._exception_handler.handle_geocode_exceptions(exc)

    def _get_image_links(self, name: str) -> list[str]:
        items: list[dict[str, Any]] = self._naver_client.get_images(name)
        return [
            item.get("link")
            for item in items
            if item.get("link").startswith("https://")
        ]

    def create_restaurant(
        self, name: str, address: str, category: str, ip_address: str, review=None
    ) -> CreateRestaurantDto:
        self._validator.validate_duplicate_restaurant(name, address, ip_address)
        self._validator.validate_category(category)

        x, y, distance = self._get_geocode_data(address)
        if Restaurant.objects.filter(
            name=name, address=address, detail_address=name
        ).exists():
            restaurant: Restaurant = Restaurant.objects.get(
                name=name, address=address, detail_address=name
            )
            restaurant.suggested_count += 1
            restaurant.save()
        else:
            restaurant = Restaurant.objects.create(
                name=name,
                address=address,
                detail_address=name,
                category=category,
                longitude=x,
                latitude=y,
                far_from_lions_park=distance / self.METERS_PER_KM,
            )

        if review:
            Review.objects.create(restaurant=restaurant, post=review)

        IPAddress.objects.create(restaurant=restaurant, ip_address=ip_address)

        images: list[str] = self._get_image_links(name)
        if images:
            RestaurantImage.objects.bulk_create(
                [
                    RestaurantImage(
                        restaurant=restaurant,
                        img_url=image,
                    )
                    for image in images
                ],
            )
        return CreateRestaurantDto(count=restaurant.suggested_count)
