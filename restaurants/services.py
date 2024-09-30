from datetime import datetime
from typing import Any, Final

from django.utils import timezone

from exceptions import (
    AlreadyAddRestaurantException,
    ApplicationAuthenticationFailedException,
    AuthenticationFailedException,
    CategoryNotFoundException,
    DistanceTooFarException,
    IncorrectQueryRequestException,
    InternalServerErrorException,
    InvalidDisplayValueException,
    InvalidParameterException,
    InvalidRequestException,
    InvalidSearchAPIException,
    InvalidSortValueException,
    InvalidStartValueException,
    MalformedEncodingException,
    NotFoundException,
    SystemErrorException,
    UnknownNaverException,
)
from restaurants.dtos import CreateRestaurantDto, SearchRestaurantsDto
from restaurants.models import Restaurant, RestaurantImage, Review
from utils.clients import NaverClient
from utils.parsers import remove_html_tags


class RestaurantService:
    DAEGU_PREFIX: Final[str] = "대구광역시"
    GYUNGSAN_PREFIX: Final[str] = "경상북도 경산시"
    RESTAURANT_ADD_COOLDOWN_DAYS: Final[int] = 3
    METERS_PER_KM: Final[int] = 1000

    def __init__(self):
        self._naver_client: NaverClient = NaverClient()

    def _filter_daegu_gyungsan_restaurants(self, restaurants: dict[str, Any]) -> list[str]:
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
        name: str = remove_html_tags(restaurant.get("title", ""))
        road_address: str = self._clean_road_address(name, restaurant.get("roadAddress", ""))
        return SearchRestaurantsDto(name=name, road_address=road_address)

    def _handle_search_exceptions(self, exception: Exception) -> None:
        exception_mapping: dict[Exception, Exception] = {
            (
                DistanceTooFarException,
                InvalidDisplayValueException,
                IncorrectQueryRequestException,
                InvalidStartValueException,
                InvalidSortValueException,
                MalformedEncodingException,
                UnknownNaverException,
            ): InvalidRequestException,
            AuthenticationFailedException: ApplicationAuthenticationFailedException,
            InvalidSearchAPIException: NotFoundException,
            SystemErrorException: InternalServerErrorException,
        }

        for exception_types, mapped_exception in exception_mapping.items():
            if isinstance(exception, exception_types):
                raise mapped_exception(str(exception))

        raise exception

    def search_restaurants(self, name: str) -> list[SearchRestaurantsDto]:
        try:
            restaurants = self._naver_client.search_places(name=name)
        except Exception as exc:
            self._handle_search_exceptions(exc)

        daegu_gyungsan_restaurants: list[str] = self._filter_daegu_gyungsan_restaurants(restaurants)
        search_results: list[SearchRestaurantsDto] = [
            self._create_search_dto(restaurant) for restaurant in daegu_gyungsan_restaurants
        ]

        if not search_results:
            raise NotFoundException("해당하는 식당이 없습니다.")

        return search_results

    def _check_duplicate_restaurant(self, name: str, address: str, ip_address: str) -> None:
        cooldown_date: datetime = timezone.now() - timezone.timedelta(
            days=self.RESTAURANT_ADD_COOLDOWN_DAYS
        )
        if Restaurant.objects.filter(
            name=name,
            address=address,
            detail_address=name,
            ip_address=ip_address,
            created__gte=cooldown_date,
        ).exists():
            raise AlreadyAddRestaurantException(
                f"같은 식당은 {self.RESTAURANT_ADD_COOLDOWN_DAYS}일에 1번만 추천할 수 있습니다."
            )

    def _validate_category(self, category: str) -> None:
        if category not in Restaurant.RestaurantType.values:
            raise CategoryNotFoundException("해당하는 카테고리를 찾을 수 없습니다.")

    def _validate_distance(self, distance: float) -> None:
        if distance > 20:
            raise DistanceTooFarException("라팍과의 직선 거리가 20km 초과입니다.")

    def _get_geocode_data(self, address: str) -> tuple[str, str, float]:
        try:
            return self._naver_client.get_geocode_distance_by_address(address=address)
        except InvalidParameterException as exc:
            raise InvalidRequestException(str(exc))
        except SystemErrorException as exc:
            raise InternalServerErrorException(str(exc))

    def _get_image_links(self, name: str) -> list[str]:
        items: list[dict[str, Any]] = self._naver_client.get_images(name)
        return [
            item.get("link")
            for item in items
            if item.get("link").startswith("https://")
        ]

    def create_restaurant(
        self,
        name: str,
        address: str,
        category: str,
        ip_address: str,
        review: str | None = None,
    ) -> CreateRestaurantDto:
        self._check_duplicate_restaurant(name, address, ip_address)
        self._validate_category(category)

        x, y, distance = self._get_geocode_data(address)
        distance = distance / self.METERS_PER_KM
        self._validate_distance(distance=distance)

        restaurant: Restaurant = Restaurant.objects.create(
            name=name,
            address=address,
            detail_address=name,
            ip_address=ip_address,
            category=category,
            longitude=x,
            latitude=y,
            far_from_lions_park=distance / self.METERS_PER_KM,
        )

        if review:
            Review.objects.create(restaurant=restaurant, post=review)

        images: list[str] = self._get_image_links({name})
        if images:
            RestaurantImage.objects.bulk_create(
                [
                    RestaurantImage(
                        restaurant=restaurant,
                        img_url=image,
                    )
                    for image in images
                ]
            )

        restaurant_count: int = Restaurant.objects.filter(
            name=name, address=address, detail_address=name
        ).count()
        return CreateRestaurantDto(count=restaurant_count)
