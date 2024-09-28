from rest_framework import serializers

from restaurants.models import Restaurant, RestaurantImage, Review


class ListRestaurantSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_count(self, obj) -> int:
        return Restaurant.objects.filter(name=obj.name).count()

    def get_reviews(self, obj) -> list[str]:
        if hasattr(obj, "review_posts"):
            return [
                review.post
                for review in Review.objects.select_related("restaurant").filter(
                    restaurant__name=obj.name
                )
            ]
        return []

    def get_images(self, obj) -> list[str]:
        return [
            restaurant_image.img_url
            for restaurant_image in RestaurantImage.objects.select_related("restaurant")
            .filter(restaurant__name=obj.name)
            .order_by("-created")[:2]
        ]


class SearchRestaurantsResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    road_address = serializers.CharField()


class SearchRestaurantsQuerySerializer(serializers.Serializer):
    name = serializers.CharField()


class CreateRestaurantRequestSerializer(serializers.ModelSerializer):
    review = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = Restaurant
        fields = ("name", "address", "category", "review")


class CreateRestaurantResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
