from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from apps.common.models import BaseModel


class User(BaseModel, AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Administrator")
        USER = ("user", "User")
    ...
