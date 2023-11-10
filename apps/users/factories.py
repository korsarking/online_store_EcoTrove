import factory
from factory.django import DjangoModelFactory

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("word")
    date_of_birth = factory.Faker("date")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number", locale="hi_IN")
    is_active = False
