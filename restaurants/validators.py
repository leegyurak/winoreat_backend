from datetime import datetime
from typing import Final

from django.db.models import Exists, OuterRef
from django.utils import timezone

from exceptions import (
    AlreadyAddRestaurantException,
    CategoryNotFoundException,
    TooFarFromLionsParkException,
)
from restaurants.models import IPAddress, Restaurant


class RestaurantValidator:
    RESTAURANT_ADD_COOLDOWN_DAYS: Final[int] = 3
    MAXIMUM_DISTANCE_TO_LIONS_PARK: Final[int] = 20

    @staticmethod
    def validate_category(category: str) -> None:
        if category not in Restaurant.RestaurantType.values:
            raise CategoryNotFoundException("해당하는 카테고리를 찾을 수 없습니다.")

    @classmethod
    def validate_distance(cls, distance: float) -> None:
        if distance > cls.MAXIMUM_DISTANCE_TO_LIONS_PARK:
            raise TooFarFromLionsParkException("라팍과의 거리가 20km를 넘습니다.")

    @classmethod
    def validate_duplicate_restaurant(
        cls, name: str, address: str, ip_address: str
    ) -> None:
        cooldown_date: datetime = timezone.now() - timezone.timedelta(
            days=cls.RESTAURANT_ADD_COOLDOWN_DAYS
        )

        ip_address_exists = IPAddress.objects.filter(
            restaurant=OuterRef('pk'),
            ip_address=ip_address
        )

        if Restaurant.objects.filter(
            name=name,
            address=address,
            detail_address=name,
            modified__gte=cooldown_date,
        ).annotate(
            has_ip=Exists(ip_address_exists)
        ).filter(has_ip=True).exists():
            raise AlreadyAddRestaurantException(
                f"같은 식당은 {cls.RESTAURANT_ADD_COOLDOWN_DAYS}일에 1번만 추천할 수 있습니다."
            )
