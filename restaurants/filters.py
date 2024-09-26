from django_filters import rest_framework as filters

from restaurants.models import Restaurant


class RestaurantFilter(filters.FilterSet):
    category = filters.ChoiceFilter(choices=Restaurant.RestaurantType.choices)
    max_range = filters.NumberFilter(
        field_name="far_from_lions_park", lookup_expr="lte"
    )

    class Meta:
        model = Restaurant
        fields = ["category", "max_range"]
