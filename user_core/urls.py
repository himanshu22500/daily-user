from django.urls import path
from user_core.views.create_user import create_user
from user_core.views.get_users import get_users
from user_core.views.delete_user import delete_user
from user_core.views.update_user import update_user

urlpatterns = [
    path("create_user", create_user),
    path("get_users", get_users),
    path("delete_user", delete_user),
    path("update_user", update_user)
]
