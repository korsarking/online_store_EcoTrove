from unittest.mock import patch

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
from apps.users.models import UserAddress

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
            "username": faker.word(),
            "date_of_birth": faker.date()
        }
        self.client.force_authenticate(user=self.active_user)
        self.assertNotEqual(data["username"], self.active_user.username)
        self.assertNotEqual(data["date_of_birth"], self.active_user.date_of_birth)

        response = self.client.patch(reverse("users:user-detail", kwargs={"id": self.active_user.id}), data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data["username"], response.data["username"])
        self.assertEqual(data["date_of_birth"], response.data["date_of_birth"])


class TestUserAddress(APITestCase):

    def setUp(self):
        self.user = UserFactory.create(password=make_password("StrongPassword"), is_active=True)
        self.user_admin = UserFactory.create(password=make_password("StrongPassword"), is_active=True, role="admin")
        self.user_address = UserAddress.objects.create(
            country="USA",
            region="Pacific Northwest",
            city="Seattle",
            street="Broadway",
            block="41",
            zipcode="98101",
            user=self.user
        )
        self.user_address2 = UserAddress.objects.create(user=self.user)

    def test_user_address_list(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("users:address-list"))

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(
            response.data["results"]),
            UserAddress.objects.filter(user=self.user).count()
        )

    def test_user_address_create(self):
        self.client.force_authenticate(self.user)
        data = {
            "country": "Republic of Moldova",
            "region": "Municipality of Chisinau",
            "city": "Chisinau",
            "street": "Stefan Cel Mare",
            "block": "33",
            "zipcode": "4650"
        }
        response = self.client.post(reverse("users:address-list"), data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_user_address_update(self):
        self.client.force_authenticate(self.user)

        new_country = "Germany"
        new_region = "Hamburg"

        data = {
            "country": new_country,
            "region": new_region,
        }

        response = self.client.patch(reverse("users:address-detail", kwargs={"pk": self.user_address.id}), data)

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_user_address_delete(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(reverse("users:address-detail", kwargs={"pk": self.user_address.id}))

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_admin_address_update(self):
        self.client.force_authenticate(self.user_admin)

        address = UserAddress.objects.create(
            country="United kingdom",
            region="England",
            city="London",
            street="Baker Street",
            block="221b",
            zipcode="48",
            user=self.user
        )

        new_country = "Greece"
        new_region = "Athene"

        data = {
            "country": new_country,
            "region": new_region,
        }

        response = self.client.patch(reverse("users:address-detail", kwargs={"pk": address.id}), data)

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_admin_address_delete(self):
        self.client.force_authenticate(self.user_admin)

        response = self.client.delete(reverse("users:address-detail", kwargs={"pk": self.user_address.id}))

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
