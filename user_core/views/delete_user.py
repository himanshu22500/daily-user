from typing import List

from rest_framework.decorators import api_view
from user_core.storages.user_storage import UserStorage
from user_core.interactor.delete_user import DeleteUserInteractor
from user_core.presenters.presenter import Presenter
from user_core.dtos import DeleteUserParamsDTO


@api_view(["POST"])
def delete_user(request):
    post_body = request.data
    delete_user_params_dto = DeleteUserParamsDTO(
        user_id=post_body.get("user_id"),
        mobile_number=post_body.get("mob_num")
    )

    user_storage = UserStorage()
    presenter = Presenter()
    interactor = DeleteUserInteractor(user_storage=user_storage)
    return interactor.delete_user_wrapper(delete_user_params_dto=delete_user_params_dto, presenter=presenter)
