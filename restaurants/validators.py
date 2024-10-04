from datetime import datetime
from typing import Final

from django.utils import timezone

from exceptions import (
    AlreadyAddRestaurantException,
    CategoryNotFoundException,
)
from restaurants.models import Restaurant


class RestaurantValidator:
    RESTAURANT_ADD_COOLDOWN_DAYS: Final[int] = 3

    @staticmethod
    def validate_category(category: str) -> None:
        if category not in Restaurant.RestaurantType.values:
            raise CategoryNotFoundException("해당하는 카테고리를 찾을 수 없습니다.")

    @classmethod
    def validate_duplicate_restaurant(cls, name: str, address: str, ip_address: str) -> None:
        cooldown_date: datetime = timezone.now() - timezone.timedelta(
            days=cls.RESTAURANT_ADD_COOLDOWN_DAYS
        )
        if Restaurant.objects.filter(
            name=name,
            address=address,
            detail_address=name,
            created__gte=cooldown_date,
            ip_addresses__ip_address=ip_address,
        ).exists():
            raise AlreadyAddRestaurantException(
                f"같은 식당은 {cls.RESTAURANT_ADD_COOLDOWN_DAYS}일에 1번만 추천할 수 있습니다."
            )
