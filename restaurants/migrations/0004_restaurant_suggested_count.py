# Generated by Django 5.1.1 on 2024-10-01 07:25

from django.db import migrations, models
from django.db.models import Count

from restaurants.models import Restaurant, RestaurantImage, Review


def set_default_suggested_count(apps, schema_editor):
    restaurant_groups = Restaurant.objects.values("name").annotate(count=Count("id"))
    for restaurant_group in restaurant_groups:
        reviews = Review.objects.filter(
            restaurant__name=restaurant_group["name"]
        )
        images = RestaurantImage.objects.filter(
            restaurant__name=restaurant_group["name"]
        )
        restaurants = Restaurant.objects.filter(name=restaurant_group["name"])
        if restaurants.filter(players_pick__isnull=False).exists():
            target_restaurant = restaurants.get(players_pick__isnull=False)
        else:
            target_restaurant = restaurants.first()
        target_restaurant.suggested_count = restaurant_group["count"]
        target_restaurant.save()
        reviews.update(restaurant=target_restaurant)
        images.update(restaurant=target_restaurant)
        restaurants.exclude(id=target_restaurant.id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0003_alter_restaurantimage_img_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="suggested_count",
            field=models.IntegerField(default=1, verbose_name="추천된 횟수"),
        ),
        migrations.RunPython(set_default_suggested_count),
    ]
