import phonenumbers
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.common.models import BaseModel


def phone_is_valid(value: str):
    try:
        phone_number_obj = phonenumbers.parse(value)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("invalid phone number.")

    if not phonenumbers.is_valid_number(phone_number_obj):
        raise ValidationError("invalid phone number.")


class User(AbstractUser, BaseModel):
    last_login = None

    class Role(models.TextChoices):
        ADMIN = ("admin", "Administrator")
        USER = ("user", "User")

    username = models.CharField(max_length=120, blank=False, unique=True)
    date_of_birth = models.DateField(null=True, default=None)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20, blank=False, unique=True, validators=[phone_is_valid]
    )
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="Users/user/PycharmProjects/profile_pic"
    )
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "username"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-id"]


class UserAddress(BaseModel):
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    block = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    class Meta:
        db_table = "addresses"
        ordering = ["-id"]
