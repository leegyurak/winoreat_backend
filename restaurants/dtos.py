from dataclasses import dataclass


@dataclass
class SearchRestaurantsDto:
    name: str
    road_address: str


@dataclass
class CreateRestaurantDto:
    count: int
