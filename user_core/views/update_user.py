from typing import List

from rest_framework.decorators import api_view
from user_core.storages.user_storage import UserStorage
from user_core.interactor.update_user import UpdateUserInteractor
from user_core.presenters.presenter import Presenter
from user_core.dtos import UpdateUserParamsDTO
from user_core.views import UpdateUserSerializer


@api_view(["POST"])
def update_user(request):
    serializer = UpdateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    post_body = request.data
    update_data = post_body["update_data"]
    update_user_params_dto = UpdateUserParamsDTO(
        user_ids=post_body["user_ids"],
        name=update_data.get("full_name"),
        mobile_number=update_data.get("mob_num") ,
        pan_number=update_data.get("pan_num"),
        manager_id=update_data.get("manager_id")
    )

    user_storage = UserStorage()
    presenter = Presenter()
    interactor = UpdateUserInteractor(user_storage=user_storage)
    return interactor.update_user_wrapper(update_user_params_dto=update_user_params_dto, presenter=presenter)
