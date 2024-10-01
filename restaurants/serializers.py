from rest_framework import serializers

from restaurants.models import Restaurant


class ReviewPostsField(serializers.RelatedField):
    def to_representation(self, value):
        return value.post


class RestaurantImageUrlsField(serializers.RelatedField):
    def to_representation(self, value):
        return value.img_url


class ListRestaurantSerializer(serializers.ModelSerializer):
    review_posts = ReviewPostsField(source="reviews", many=True, read_only=True)
    image_urls = RestaurantImageUrlsField(source="images", many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = "__all__"


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
