from django.urls import path
from user_core.views.create_user import create_user
from django.conf import settings

urlpatterns = [
    path("create_user", create_user),
]
