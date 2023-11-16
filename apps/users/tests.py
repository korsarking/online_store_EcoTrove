from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory
from apps.users.models import User

faker = Faker()


def fake_phone_number(fake: Faker) -> str:
    return f"+373 78{fake.msisdn()[7:]}"


class UserTestCase(APITestCase):

    def setUp(self):
        self.active_user = UserFactory.create(password=make_password("StrongPassword"), is_active=True)
        self.inactive_user = UserFactory.create(password=make_password("StrongPassword"))

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

        response = self.client.post(reverse("users:user-list"), data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        user = User.objects.get(email=data["email"])

        self.assertEqual(user.email, data["email"])
        self.assertFalse(user.is_active)

    def test_verify_user(self):
        a = {
            "uid": utils.encode_uid(self.inactive_user.pk),
            "token": default_token_generator.make_token(self.inactive_user)
        }

        response = self.client.post(reverse("users:user-activation"), {"uid": a["uid"], "token": a["token"]})
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.inactive_user.refresh_from_db()
        self.assertTrue(self.inactive_user.is_active)

    def test_user_invalid_number_negative(self):
        data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "username": faker.word(),
            "password": make_password("StrongPassword"),
            "is_active": False,
            "phone": "Some_Random_Symbols"
        }
        response = self.client.post(reverse("users:user-list"), data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_user_nonexistent_number_negative(self):
        data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "username": faker.word(),
            "password": make_password("StrongPassword"),
            "is_active": False,
            "phone": "+123456789012345"
        }
        response = self.client.post(reverse("users:user-list"), data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_users_list(self):
        self.client.force_authenticate(user=self.active_user)

        response = self.client.get(reverse("users:user-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("count"), User.objects.count())
        response_full_name = f"{response.data["results"][1]["first_name"]} {response.data["results"][1]["last_name"]}"
        expected_full_name = f"{self.active_user.first_name} {self.active_user.last_name}"
        self.assertEqual(response_full_name, expected_full_name)

    def test_update_user_data(self):
        data = {
            "phone": fake_phone_number(faker)
        }
        self.client.force_authenticate(user=self.active_user)
        self.assertNotEqual(data["phone"], self.active_user.phone)

        response = self.client.patch(reverse("users:user-me"), data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data["phone"], response.data["phone"])

    def test_update_user_data_by_id(self):
        data = {
            "username": faker.word()
        }
        self.client.force_authenticate(user=self.active_user)
        self.assertNotEqual(data["username"], self.active_user.username)

        response = self.client.patch(reverse("users:user-detail", kwargs={"id": self.active_user.id}), data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data["username"], response.data["username"])
