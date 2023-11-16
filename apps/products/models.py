import datetime

from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.db import models

from apps.users.models import User
from apps.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255)
    img = models.ImageField(null=True)

    class Meta:
        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["-id"]


class SubCategory(BaseModel):
    name = models.CharField(max_length=255)
    img = models.ImageField(null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "sub_category"
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"
        ordering = ["-id"]


class Product(BaseModel):
    deleted_at = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    details = models.TextField(null=True, default=None)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    composition = models.CharField(max_length=255, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["-id"]

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.datetime.now()
        self.save()


class ProductReview(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(null=True, default=None)

    class Meta:
        db_table = "product_review"
        verbose_name = "review"
        verbose_name_plural = "reviews"
        ordering = ["-id"]


class ProductAttachments(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attachments"
    )
    attachment = models.ImageField(upload_to="products/attachments")

    class Meta:
        ordering = ["-id"]
