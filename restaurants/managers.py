from django.db import models

from restaurants.querysets import RestaurantQuerySet


class RestaurantManager(models.Manager):
    def get_queryset(self):
        return RestaurantQuerySet(self.model, using=self._db)

    def get_filtered_restaurants(self):
        return (
            self.get_queryset()
            .with_full_address()
            .with_address_count()
            .with_review_count()
            .with_player_pick()
            .get_latest_or_player_pick_by_full_address()
            .order_by_criteria()
            .with_review_posts()
        )
