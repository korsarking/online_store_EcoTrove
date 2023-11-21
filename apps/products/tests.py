import os.path
import shutil

from django.core.files.uploadedfile import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.factories import CategoryFactory
from apps.products.factories import ProductAttachmentsFactory
from apps.products.factories import ProductFactory
from apps.products.factories import ProductReviewFactory
from apps.users.factories import UserFactory
from apps.users.models import User
from config.settings import MEDIA_FOR_TESTING_ROOT
from config.settings import MEDIA_ROOT

TEST_DIR = os.path.join(MEDIA_ROOT, "testing")


@override_settings(MEDIA_ROOT=TEST_DIR)
class TestProduct(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_DIR)

    def setUp(self) -> None:
        self.user = UserFactory(role=User.Role.USER, is_active=True)
        self.admin = UserFactory(role=User.Role.ADMIN, is_active=True)

        self.product1 = ProductFactory.create()
        self.product2 = ProductFactory.create()

    def test_products_get(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("products:product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_negative(self):
        self.client.force_authenticate(self.user)

    def test_user_update_negative(self):
        self.client.force_authenticate(self.user)

        data = {"price": 0}
        response = self.client.patch(
            reverse("products:product-detail", kwargs={"pk": self.product1.id}), data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_negative(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse("products:product-detail", kwargs={"pk": self.product1.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_post(self):
        self.client.force_authenticate(self.admin)

        data = {"name": "test1", "price": 9, "discount": 12, "specs": "Promo"}

        response = self.client.post(reverse("products:product-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_post_invalid_discount(self):
        self.client.force_authenticate(self.admin)

        data = {"name": "test1", "price": 9, "discount": -2}

        response = self.client.post(reverse("products:product-list"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"name": "test1", "price": 9, "discount": 200}

        response = self.client.post(reverse("products:product-list"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            reverse("products:product-detail", kwargs={"pk": self.product1.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_update(self):
        self.client.force_authenticate(self.admin)

        data = {"discount": 20}
        response = self.client.patch(
            reverse("products:product-detail", kwargs={"pk": self.product1.id}), data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


@override_settings(MEDIA_ROOT=TEST_DIR)
class TestProductAttachments(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(role=User.Role.USER, is_active=True)
        self.admin = UserFactory(role=User.Role.ADMIN, is_active=True)

        self.product = ProductFactory.create()

        self.img_path = os.path.join(MEDIA_FOR_TESTING_ROOT, "green_square.jpg")
        self.img = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(self.img_path, "rb").read(),
            content_type="image/jpeg",
        )
        self.attachment = ProductAttachmentsFactory.create(
            product=self.product, attachment=self.img
        )

    def test_user_get(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("products:attachments-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_filtered_product(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse("products:attachments-list"), {"product": self.product.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_user_post_negative(self):
        self.client.force_authenticate(self.user)

        data = {"product": 1, "attachment": self.img}

        response = self.client.post(reverse("products:attachments-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_negative(self):
        self.client.force_authenticate(self.user)

        img = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(self.img_path, "rb").read(),
            content_type="image/jpeg",
        )
        data = {"product": 1, "attachment": img}

        response = self.client.patch(
            reverse("products:attachments-detail", kwargs={"pk": self.product.id}),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse("products:attachments-detail", kwargs={"pk": self.attachment.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_post(self):
        self.client.force_authenticate(self.admin)

        img = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(self.img_path, "rb").read(),
            content_type="image/jpeg",
        )

        data = {"product": self.product.id, "attachment": img}

        response = self.client.post(reverse("products:attachments-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_update(self):
        self.client.force_authenticate(self.admin)

        attachment = self.product.attachments.create(
            attachment=File("/media/test/green_square.jpg")
        )

        img = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(self.img_path, "rb").read(),
            content_type="image/jpeg",
        )
        data = {"attachment": img}

        response = self.client.patch(
            reverse("products:attachments-detail", kwargs={"pk": attachment.id}),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            reverse("products:attachments-detail", kwargs={"pk": self.attachment.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


@override_settings(MEDIA_ROOT=TEST_DIR)
class TestCategory(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_DIR)

    def setUp(self) -> None:
        self.user = UserFactory(role=User.Role.USER, is_active=True)
        self.admin = UserFactory(role=User.Role.ADMIN, is_active=True)

        self.product = ProductFactory.create()

        self.category = CategoryFactory.create(name="test")

    def test_user_get(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("products:category-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_negative(self):
        self.client.force_authenticate(self.user)

        data = {
            "name": 1,
        }

        response = self.client.post(reverse("products:category-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_negative(self):
        self.client.force_authenticate(self.user)

        data = {"name": 1}

        response = self.client.patch(
            reverse("products:category-detail", kwargs={"pk": self.product.id}),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse("products:category-detail", kwargs={"pk": self.category.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_post(self):
        self.client.force_authenticate(self.admin)

        data = {"name": "test1"}

        response = self.client.post(reverse("products:category-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_update(self):
        self.client.force_authenticate(self.admin)

        data = {"name": "test1"}

        response = self.client.patch(
            reverse("products:category-detail", kwargs={"pk": self.category.id}),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            reverse("products:category-detail", kwargs={"pk": self.category.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


@override_settings(MEDIA_ROOT=TEST_DIR)
class TestProductReview(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_DIR)

    def setUp(self) -> None:
        self.user = UserFactory(role=User.Role.USER, is_active=True)
        self.user2 = UserFactory(role=User.Role.USER, is_active=True)
        self.admin = UserFactory(role=User.Role.ADMIN, is_active=True)

        self.product = ProductFactory.create()

        self.review = ProductReviewFactory.create(
            user=self.user, rating=3, product=self.product
        )

    def test_user_get(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("products:review-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post(self):
        self.client.force_authenticate(self.user)

        data = {"product": self.product.id, "text": "text", "rating": 4}

        response = self.client.post(reverse("products:review-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_update(self):
        self.client.force_authenticate(self.user)

        data = {"product": self.product.id, "text": "text!", "rating": 2}

        response = self.client.patch(
            reverse("products:review-detail", kwargs={"pk": self.review.id}), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse("products:review-detail", kwargs={"pk": self.review.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_update_foreign_review_negative(self):
        self.client.force_authenticate(self.user2)

        data = {"product": self.product.id, "text": "text!", "rating": 2}

        response = self.client.patch(
            reverse("products:review-detail", kwargs={"pk": self.review.id}), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_foreign_review_negative(self):
        self.client.force_authenticate(self.user2)

        response = self.client.delete(
            reverse("products:review-detail", kwargs={"pk": self.review.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_update_foreign_review(self):
        self.client.force_authenticate(self.admin)

        data = {"product": self.product.id, "text": "[REDACTED]", "rating": 2}

        response = self.client.patch(
            reverse("products:review-detail", kwargs={"pk": self.review.id}), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            reverse("products:review-detail", kwargs={"pk": self.review.id})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
