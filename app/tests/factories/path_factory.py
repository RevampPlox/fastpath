from factory.base import Factory
from factory.declarations import List, SubFactory

from app.tests.factories.coordinates_factory import (
    CoordinatesRequestFactory,
)


class PathRequestFactory(Factory):
    class Meta:
        model = dict

    pickup = SubFactory(CoordinatesRequestFactory)
    dropoff = List([SubFactory(CoordinatesRequestFactory) for _ in range(5)])
