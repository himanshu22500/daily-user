from typing import List

from rest_framework.decorators import api_view
from user_core.storages.user_storage import UserStorage
from user_core.interactor.get_users import GetUsersInteractor
from user_core.presenters.presenter import Presenter
from user_core.dtos import GetUsersParamsDTO


@api_view(["POST"])
def get_users(request):
    post_body = request.data

    user_dto = GetUsersParamsDTO(
        user_id=post_body.get("user_id"),
        manager_id=post_body.get("manager_id"),
        mobile_number=post_body.get("mob_num"),
    )

    user_storage = UserStorage()
    presenter = Presenter()
    interactor = GetUsersInteractor(user_storage=user_storage)
    return interactor.get_users_wrapper(get_users_params=user_dto, presenter=presenter)
