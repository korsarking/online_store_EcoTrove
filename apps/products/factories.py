import random

import factory
from factory.django import DjangoModelFactory

from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductAttachments
from apps.products.models import ProductReview
from apps.products.models import SubCategory
from apps.users.factories import UserFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    img = factory.django.ImageField(color="blue")


class SubCategoryFactory(DjangoModelFactory):
    class Meta:
        model = SubCategory

    name = factory.Faker("word")
    img = factory.django.ImageField(color="green")
    category = factory.SubFactory(CategoryFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    deleted_at = factory.Faker("pybool")
    name = factory.Faker("word")
    details = factory.Faker("text")
    price = round(random.uniform(1, 6666), 2)
    discount = random.randint(0, 99)
    composition = factory.Faker("text")
    sub_category = factory.SubFactory(SubCategoryFactory)


class ProductReviewFactory(DjangoModelFactory):
    class Meta:
        model = ProductReview

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    rating = random.randint(1, 5)
    text = factory.Faker("text")


class ProductAttachmentsFactory(DjangoModelFactory):
    class Meta:
        model = ProductAttachments

    product = factory.SubFactory(ProductFactory)
    attachment = factory.django.ImageField(color="red")
