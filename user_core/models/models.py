from django.db import models
from uuid import uuid4
from django.utils import timezone

class User(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, max_length=255)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, unique=True)
    pan_number = models.CharField(max_length=20, unique=True)
    manager_id = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
