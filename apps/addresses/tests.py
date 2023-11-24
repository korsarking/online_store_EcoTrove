from django.contrib.auth.hashers import make_password
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from apps.addresses.factories import AddressFactory
from apps.addresses.models import Address
from apps.users.factories import UserFactory

faker = Faker()


class TestAddress(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(
            password=make_password("StrongPassword"), is_active=True
        )
        self.user_address = AddressFactory.create()
        self.user.addresses.add(self.user_address)

    def test_user_address_create(self):
        self.client.force_authenticate(self.user)
        data = {
            "country": "Republic of Moldova",
            "region": "Municipality of Chisinau",
            "city": "Chisinau",
            "street": "Stefan Cel Mare",
            "block": "33",
            "zipcode": "4650",
        }
        response = self.client.post(reverse("addresses:address-list"), data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["id"], Address.objects.last().id)

    def test_user_address_list(self):
        self.user.addresses.add(self.user_address)
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("addresses:address-list"))

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]),
            Address.objects.filter(users=self.user).count(),
        )

    def test_user_address_update(self):
        self.client.force_authenticate(self.user)

        new_country = "Germany"
        new_region = "Hamburg"

        data = {
            "country": new_country,
            "region": new_region,
        }
        self.assertNotEqual(data["country"], Address.objects.first().country)

        response = self.client.patch(
            reverse("addresses:address-detail", kwargs={"pk": self.user_address.id}),
            data,
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data["country"], Address.objects.first().country)

    def test_user_address_delete(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse("addresses:address-detail", kwargs={"pk": self.user_address.id})
        )

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
