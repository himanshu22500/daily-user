from typing import List

from django.http import HttpResponse

from user_core.dtos import GetUsersParamsDTO, UserDTO
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface


class GetUsersInteractor:
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage


    def get_users_wrapper(self, get_users_params:GetUsersParamsDTO, presenter:PresenterInterface) -> HttpResponse:
        try:
            user_dtos = self.get_users(get_users_params=get_users_params)
        except Exception:
            pass
        else:
            return presenter.get_response_for_get_users(user_dtos=user_dtos)

    def get_users(self, get_users_params:GetUsersParamsDTO) -> List[UserDTO]:
        # todo : add validations for invalid manager_id, user_id and mobile_number
        user_dtos = self.user_storage.filter_users(get_users_params=get_users_params)
        return user_dtos