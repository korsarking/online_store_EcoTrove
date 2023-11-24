from django.db import models

from apps.common.models import BaseModel


class Log(BaseModel):
    event_type = models.CharField(max_length=32)
    details = models.JSONField()
    error_message = models.TextField(null=True)

    class Meta:
        ordering = ["-id"]
