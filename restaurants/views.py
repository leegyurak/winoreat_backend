from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, NotFound, ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from exceptions import (
    AlreadyAddRestaurantException,
    ApplicationAuthenticationFailedException,
    CategoryNotFoundException,
    InternalServerErrorException,
    InvalidRequestException,
    NotFoundException,
)
from restaurants.dtos import CreateRestaurantDto, SearchRestaurantsDto
from restaurants.filters import RestaurantFilter
from restaurants.models import Restaurant
from restaurants.serializers import (
    CreateRestaurantRequestSerializer,
    CreateRestaurantResponseSerializer,
    ListRestaurantSerializer,
    SearchRestaurantsQuerySerializer,
    SearchRestaurantsResponseSerializer,
)
from restaurants.services import RestaurantService


class ListRestaurantView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ListRestaurantSerializer
    filterset_class = RestaurantFilter
    queryset = Restaurant.objects.all().order_by('far_from_lions_park', 'players_pick')


class SearchRestaurantsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        query_serializer: SearchRestaurantsQuerySerializer = (
            SearchRestaurantsQuerySerializer(data=request.query_params)
        )
        query_serializer.is_valid(raise_exception=True)

        try:
            search_restaurants: list[
                SearchRestaurantsDto
            ] = RestaurantService().search_restaurants(
                name=query_serializer.validated_data["name"],
            )
        except InvalidRequestException as exc:
            raise ValidationError(detail=str(exc)) from exc
        except ApplicationAuthenticationFailedException as exc:
            raise NotAuthenticated(detail=str(exc)) from exc
        except NotFoundException as exc:
            raise NotFound(detail=str(exc)) from exc
        except InternalServerErrorException as exc:
            return Response([str(exc)], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer: SearchRestaurantsResponseSerializer = (
            SearchRestaurantsResponseSerializer(search_restaurants, many=True)
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class CreateRestaurantView(GenericAPIView):
    serializer_class = CreateRestaurantRequestSerializer
    queryset = Restaurant.objects.all()

    @transaction.atomic
    def post(self, request: Request) -> Response:
        request_serializer: CreateRestaurantRequestSerializer = self.get_serializer(
            data=request.data,
        )
        request_serializer.is_valid(raise_exception=True)
        try:
            restaurant: CreateRestaurantDto = RestaurantService().create_restaurant(
                **request_serializer.validated_data,
                ip_address=(
                    request.META.get("HTTP_X_FORWARDED_FOR").split(",")[0]
                    if request.META.get("HTTP_X_FORWARDED_FOR")
                    else request.META.get("REMOTE_ADDR")
                ),
            )
        except (
            InvalidRequestException,
            AlreadyAddRestaurantException,
        ) as exc:
            raise ValidationError(detail=str(exc)) from exc
        except CategoryNotFoundException as exc:
            raise NotFound(detail=str(exc)) from exc
        except InternalServerErrorException as exc:
            return Response([str(exc)], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response_serializer: CreateRestaurantResponseSerializer = (
            CreateRestaurantResponseSerializer(restaurant)
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
