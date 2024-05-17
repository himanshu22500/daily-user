from django.urls import path
from user_core.views.create_user import create_user
from user_core.views.get_users import get_users
from django.conf import settings

urlpatterns = [
    path("create_user", create_user),
    path("get_users", get_users)
]
