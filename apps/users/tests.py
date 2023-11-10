from django.contrib.auth.hashers import make_password
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory
from apps.users.models import User

faker = Faker()


def fake_phone_number(fake: Faker) -> str:
    return f"+373 78{fake.msisdn()[7:]}"


class UserTestCase(APITestCase):
    def test_register_user(self):
        data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "username": faker.word(),
            "password": make_password("StrongPassword"),
            "email": faker.email(),
            "phone": fake_phone_number(faker),
            "is_active": False,
        }

        response = self.client.post(reverse("user-list"), data=data)
        self.assertEqual(HTTP_201_CREATED, response.status_code)

        user = User.objects.get(email=data["email"])

        self.assertEqual(user.email, data["email"])
        self.assertFalse(user.is_active)

    def test_get_user(self):
        user = UserFactory.create()

        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("count"), User.objects.count())
        response_full_name = f"{response.data['results'][0]['first_name']} {response.data['results'][0]['last_name']}"
        expected_full_name = f"{user.first_name} {user.last_name}"
        self.assertEqual(response_full_name, expected_full_name)
