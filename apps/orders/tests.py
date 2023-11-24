import os.path
import shutil

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.addresses.factories import AddressFactory
from django.test import override_settings
from apps.orders.models import Order
from apps.products.factories import ProductFactory
from apps.users.factories import UserFactory
from config.settings import MEDIA_ROOT

TEST_DIR = os.path.join(MEDIA_ROOT, "testing")


@override_settings(MEDIA_ROOT=TEST_DIR)
class TestCart(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_DIR)

    def setUp(self) -> None:
        self.user = UserFactory(is_active=True)
        self.other_user = UserFactory(is_active=True)

        self.product1 = ProductFactory.create()
        self.product2 = ProductFactory.create()

    def test_user_add_item_to_cart(self):
        self.client.force_authenticate(self.user)
        data = {"product": self.product1.id, "count": 2}

        response = self.client.post(reverse("cart-item-update"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_item_count(self):
        self.client.force_authenticate(self.user)

        item = self.user.get_user_cart(create_if_none=True).add_item(self.product1, 2)

        data = {"product": self.product1.id, "count": 10}

        response = self.client.post(reverse("cart-item-update"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(item.count, response.data["count"])

    def test_user_remove_item_from_cart(self):
        self.client.force_authenticate(self.user)

        self.user.get_user_cart(create_if_none=True).add_item(self.product1, 2)

        data = {"product": self.product1.id}

        response = self.client.post(reverse("cart-item-remove"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_items(self):
        self.client.force_authenticate(self.user)

        user_cart = self.user.get_user_cart(create_if_none=True)
        user_cart.add_item(self.product1, 2)
        user_cart.add_item(self.product2, 1)

        response = self.client.get(reverse("cart-detail", kwargs={"pk": user_cart.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)

    def test_user_add_item_invalid_count_negative(self):
        self.client.force_authenticate(self.user)
        data = {"product": self.product1.id, "count": -2}

        response = self.client.post(reverse("cart-item-update"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_add_invalid_item(self):
        self.client.force_authenticate(self.user)
        data = {"product": 999999, "count": 1}

        response = self.client.post(reverse("cart-item-update"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete_invalid_item(self):
        self.client.force_authenticate(self.user)
        self.user.get_user_cart(create_if_none=True)
        data = {"product": self.product1.id}
        response = self.client.post(reverse("cart-item-remove"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete_item_from_invalid_cart(self):
        self.client.force_authenticate(self.user)
        data = {"product": self.product1.id}
        response = self.client.post(reverse("cart-item-remove"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_clear_cart(self):
        self.client.force_authenticate(self.user)

        user_cart = self.user.get_user_cart(create_if_none=True)
        user_cart.add_item(self.product1, 2)
        user_cart.add_item(self.product2, 1)

        response = self.client.post(reverse("cart-clear"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@override_settings(MEDIA_ROOT=TEST_DIR)
class TestOrders(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_DIR)

    def setUp(self) -> None:
        self.user = UserFactory.create(is_active=True)
        self.user_address = AddressFactory.create()
        self.user.addresses.add(self.user_address)
        self.other_user = UserFactory.create(is_active=True)
        self.admin_user = UserFactory.create(is_active=True, role="admin")

        self.product1 = ProductFactory.create()
        self.product2 = ProductFactory.create()

    def test_user_get_order(self):
        self.client.force_authenticate(self.user)

        cart = self.user.get_user_cart(create_if_none=True)
        cart.add_item(self.product1, 2)
        cart.add_item(self.product2, 1)
        current_order = Order.objects.create(
            user=self.user, cart=cart, address=self.user_address
        )

        response = self.client.get(
            reverse("order-detail", kwargs={"pk": current_order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_foreign_order(self):
        self.client.force_authenticate(self.other_user)

        cart = self.user.get_user_cart(create_if_none=True)
        cart.add_item(self.product1, 2)
        cart.add_item(self.product2, 1)
        current_order = Order.objects.create(
            user=self.user, cart=cart, address=self.user_address
        )

        response = self.client.get(
            reverse("order-detail", kwargs={"pk": current_order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list_order(self):
        self.client.force_authenticate(self.user)

        cart = self.user.get_user_cart(create_if_none=True)
        cart.add_item(self.product1, 2)
        cart.add_item(self.product2, 1)
        Order.objects.create(user=self.user, cart=cart, address=self.user_address)

        response = self.client.get(reverse("order-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cancel_order(self):
        self.client.force_authenticate(self.user)

        cart = self.user.get_user_cart(create_if_none=True)
        cart.add_item(self.product1, 2)
        cart.add_item(self.product2, 1)
        current_order = Order.objects.create(
            cart=cart, user=self.user, address=self.user_address
        )

        response = self.client.post(
            reverse("order-cancel", kwargs={"pk": current_order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cancel_foreign_order(self):
        self.client.force_authenticate(self.other_user)

        cart = self.user.get_user_cart(create_if_none=True)
        cart.add_item(self.product1, 2)
        cart.add_item(self.product2, 1)
        current_order = Order.objects.create(
            cart=cart, user=self.user, address=self.user_address
        )

        response = self.client.post(
            reverse("order-cancel", kwargs={"pk": current_order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_cancel_order(self):
        self.client.force_authenticate(self.admin_user)

        cart = self.user.get_user_cart(create_if_none=True)
        cart.add_item(self.product1, 2)
        cart.add_item(self.product2, 1)
        current_order = Order.objects.create(
            cart=cart, user=self.user, address=self.user_address
        )

        response = self.client.post(
            reverse("order-cancel", kwargs={"pk": current_order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_update_order(self):
        self.client.force_authenticate(self.admin_user)

        cart = self.user.get_user_cart(create_if_none=True)
        cart.add_item(self.product1, 2)
        cart.add_item(self.product2, 1)
        current_order = Order.objects.create(
            cart=cart, user=self.user, address=self.user_address
        )

        data = {"status": Order.Status.COMPLETED}
        response = self.client.patch(
            reverse("order-update-status", kwargs={"pk": current_order.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        current_order.refresh_from_db()
        self.assertEqual(current_order.status, Order.Status.COMPLETED)
