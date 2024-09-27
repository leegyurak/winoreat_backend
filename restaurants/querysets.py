from django.db import models
from django.db.models import (
    Case,
    Count,
    IntegerField,
    Max,
    OuterRef,
    Prefetch,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Coalesce, Concat


class RestaurantQuerySet(models.QuerySet):
    def with_address_count(self):
        address_count_subquery = (
            self.filter(
                address=OuterRef("address"), detail_address=OuterRef("detail_address")
            )
            .values("address")
            .annotate(count=Count("*"))
            .values("count")
        )
        return self.annotate(address_count=Subquery(address_count_subquery))

    def with_review_count(self):
        from restaurants.models import Review

        review_count_subquery = (
            Review.objects.filter(restaurant=OuterRef("pk"))
            .values("restaurant")
            .annotate(count=Count("*"))
            .values("count")
        )
        return self.annotate(review_count=Coalesce(Subquery(review_count_subquery), 0))

    def with_player_pick(self):
        return self.annotate(
            has_player_pick=Case(
                When(players_pick__isnull=False, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )

    def with_full_address(self):
        return self.annotate(
            full_address=Concat("address", Value(" "), "detail_address")
        )

    def get_latest_by_full_address(self):
        subquery = (
            self.values("full_address").annotate(max_id=Max("id")).values("max_id")
        )
        return self.filter(id__in=Subquery(subquery))

    def order_by_criteria(self):
        return self.order_by(
            "-has_player_pick", "far_from_lions_park", "-address_count", "-review_count"
        )

    def with_review_posts(self):
        from restaurants.models import Review

        return self.prefetch_related(
            Prefetch(
                "reviews", queryset=Review.objects.only("post"), to_attr="review_posts"
            )
        )
