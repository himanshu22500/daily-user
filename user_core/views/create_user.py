from typing import List

from rest_framework.decorators import api_view
from user_core.storages.user_storage import UserStorage
from user_core.dtos import UserDTO
from rest_framework.response import Response
from user_core.interactor.create_user import CreateUserInteractor
from user_core.presenters.presenter import Presenter
from user_core.dtos import UserDTO


@api_view(["POST"])
def create_user(request):
    post_body = request.data
    user_dto = UserDTO(
        name="",
        user_id="",
        manager_id="",
        mobile_number="",
        pan_number=""
    )

    user_storage = UserStorage()
    presenter = Presenter()
    interactor = CreateUserInteractor(user_storage=user_storage)
    return interactor.create_user_wrapper(user_dtos=[user_dto], presenter=presenter)
