import uuid
from django.db import models


class TimeStampedModel(models.Model):
    """Model which has UUID field as id and psudo primary key as pkid. This model also has created_at and updated_at fields"""

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
