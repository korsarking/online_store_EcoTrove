import factory
import random
from factory.django import DjangoModelFactory

from apps.addresses.models import Address


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    country = factory.Faker("word")
    region = factory.Faker("word")
    city = factory.Faker("word")
    street = factory.Faker("word")
    block = random.randint(1, 99)
    zipcode = random.randint(1, 9999)
