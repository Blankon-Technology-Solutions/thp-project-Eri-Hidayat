from django.db import models

from core.models import BaseModel


class TokenKey(BaseModel):
    key = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
