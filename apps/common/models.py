from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="Sets creation date")
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Sets the data update date"
    )

    class Meta:
        abstract = True
