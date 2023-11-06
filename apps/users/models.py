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


class User(BaseModel, AbstractUser):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Administrator")
        USER = ("user", "User")

    first_name = models.CharField(max_length=120, blank=False)
    last_name = models.CharField(max_length=120, blank=False)
    username = models.CharField(max_length=120, blank=False, unique=True)
    date_of_birth = models.DateField(null=True, default=None)
    phone = models.CharField(
        max_length=20, blank=False, unique=True, validators=[phone_is_valid]
    )
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="Users/user/PycharmProjects/profile_pic"
    )
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=False)
    last_login = None
    groups = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "username"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-id"]
