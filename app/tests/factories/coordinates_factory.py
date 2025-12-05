from factory.base import Factory
from factory.declarations import LazyFunction
from faker import Faker

fake = Faker()
fake.seed_instance(0)


class CoordinatesRequestFactory(Factory):
    class Meta:
        model = dict

    lat = LazyFunction(lambda: float(fake.latitude()))
    lng = LazyFunction(lambda: float(fake.longitude()))
