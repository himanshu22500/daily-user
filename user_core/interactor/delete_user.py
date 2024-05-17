from django.http import HttpResponse

from user_core.dtos import DeleteUserParamsDTO
from user_core.exceptions.expections import NoMatchingUserFound
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface


class DeleteUserInteractor:
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage

    def delete_user_wrapper(self, delete_user_params_dto:DeleteUserParamsDTO, presenter:PresenterInterface) -> HttpResponse:
        try:
            user_id = self.delete_user(delete_user_params_dto=delete_user_params_dto)
        except NoMatchingUserFound:
            return presenter.get_no_user_deleted_http_error()
        else:
            return presenter.get_response_for_delete_user(user_id=user_id)

    def delete_user(self, delete_user_params_dto:DeleteUserParamsDTO) -> str:
        # todo : add validation for invalid user_id and mobile_number
        user_id = self.user_storage.delete_user(delete_user_params=delete_user_params_dto)
        if not user_id:
            raise NoMatchingUserFound()

        return user_id