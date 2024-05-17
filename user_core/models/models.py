from django.db import models
from uuid import uuid4

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    pan_number = models.CharField(max_length=20)
    manager_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
