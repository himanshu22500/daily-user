from typing import List

from rest_framework.decorators import api_view
from user_core.storages.user_storage import UserStorage
from user_core.interactor.create_user import CreateUserInteractor
from user_core.presenters.presenter import Presenter
from user_core.dtos import CreateUserParamsDTO


@api_view(["POST"])
def create_user(request):
    post_body = request.data
    user_dto = CreateUserParamsDTO(
        name=post_body["full_name"],
        manager_id=post_body.get("manager_id"),
        mobile_number=post_body["mob_num"],
        pan_number=post_body["pan_num"]
    )

    user_storage = UserStorage()
    presenter = Presenter()
    interactor = CreateUserInteractor(user_storage=user_storage)
    return interactor.create_user_wrapper(user_dto=user_dto, presenter=presenter)
