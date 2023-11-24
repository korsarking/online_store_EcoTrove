from django.db import models

from apps.common.models import BaseModel


class Address(BaseModel):
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    block = models.CharField(max_length=1000)
    zipcode = models.CharField(max_length=10000)

    class Meta:
        db_table = "addresses"
        verbose_name = "address"
        verbose_name_plural = "addresses"
        ordering = ["id"]
