import phonenumbers
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.addresses.models import Address
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
        null=True, blank=True, upload_to="users/profile_pic"
    )
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    addresses = models.ManyToManyField(Address, blank=True, related_name="users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "username"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-id"]

    def get_user_cart(self, create_if_none=False):
        if cart := self.carts.filter(is_archived=False).first():
            return cart

        if create_if_none:
            cart = self.carts.create(is_archived=False)
        else:
            raise ValidationError({"cart": "Current user has no cart."})

        return cart
