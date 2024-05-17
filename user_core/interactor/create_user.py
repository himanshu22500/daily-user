from django.http import HttpResponse

from user_core.dtos import UserDTO, CreateUserParamsDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface


class CreateUserInteractor:
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage

    def create_user_wrapper(self, user_dto:CreateUserParamsDTO, presenter:PresenterInterface) -> HttpResponse:
        try:
            user_dto = self.create_user(user_dto=user_dto)
        except Exception:
            return presenter.get_error_http()

        return presenter.get_response_for_create_user(user_dto=user_dto)

    def create_user(self, user_dto:CreateUserParamsDTO) -> UserDTO:
        # todo : add validations
        user_dto = self.user_storage.create_users(user_dtos=[user_dto])
        return user_dto[0]