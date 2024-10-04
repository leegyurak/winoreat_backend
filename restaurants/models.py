from django.db import models
from django_extensions.db.models import TimeStampedModel

from restaurants.managers import RestaurantManager


class Restaurant(TimeStampedModel):
    class RestaurantType(models.TextChoices):
        KOREAN = "KOREAN", "한식"
        JAPANESE = "JAPANESE", "일식"
        CHINESE = "CHINESE", "중식"
        WESTERN_FOOD = "WESTERN_FOOD", "양식"
        MEAT = "MEAT", "고기"
        FRIED_CHICKEN = "FRIED_CHICKEN", "치킨"
        CHICKEN = "CHICKEN", "닭요리"
        FISH = "FISH", "물고기"
        DRINK = "DRINK", "술집"
        CAFE = "CAFE", "카페"

    name = models.CharField(verbose_name="식당 이름", max_length=63)
    address = models.CharField(verbose_name="식당 주소", max_length=1023)
    detail_address = models.CharField(
        verbose_name="식당 상세 주소",
        max_length=127,
        null=True,
        blank=True,
        db_index=True,
    )
    longitude = models.FloatField(verbose_name="경도")
    latitude = models.FloatField(verbose_name="위도")
    far_from_lions_park = models.FloatField(
        verbose_name="라팍과의 직선 거리", db_index=True
    )
    category = models.CharField(
        verbose_name="카테고리", choices=RestaurantType.choices, max_length=63
    )
    players_pick = models.CharField(
        verbose_name="이 가게를 고른 선수 이름", max_length=15, null=True, blank=True
    )
    suggested_count = models.IntegerField(verbose_name="추천된 횟수", default=1)

    objects = RestaurantManager()


class Review(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name="식당 id",
        related_name="reviews",
    )
    post = models.TextField()


class RestaurantImage(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name="식당 id",
        related_name="images",
    )
    img_url = models.URLField(max_length=4095)


class IPAddress(TimeStampedModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name="식당 id",
        related_name="ip_addresses",
    )
    ip_address = models.CharField(verbose_name="작성자 IP", max_length=63)
