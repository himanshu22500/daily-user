from django.http import HttpResponse

from user_core.dtos import UserDTO, CreateUserParamsDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
from user_core.exceptions.expections import FullNameCanNotBeEmpty, InvalidMobileNumber, InvalidManagerId, \
    ManagerDoesNotExists, DeactivatedManager
from user_core.interactor.validation_mixin import ValidationMixin


class CreateUserInteractor(ValidationMixin):
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage

    def create_user_wrapper(self, user_dto:CreateUserParamsDTO, presenter:PresenterInterface) -> HttpResponse:
        try:
            user_dto = self.create_user(user_dto=user_dto)
        except FullNameCanNotBeEmpty:
            return presenter.get_empty_full_name_http_error()
        except InvalidMobileNumber as err:
            return presenter.get_invalid_mobile_number_http_error(mobile_number=err.mobile_number)
        except ManagerDoesNotExists as err:
            return presenter.get_manager_not_found_http_error(manager_id=err.manager_id)
        except InvalidManagerId as err:
            return presenter.get_manager_not_found_http_error(manager_id=err.manager_id)
        except DeactivatedManager as err:
            return presenter.get_deactivated_manager_id_http_error(manager_id=err.manager_id)
        else:
            return presenter.get_response_for_create_user(user_dto=user_dto)

    def create_user(self, user_dto:CreateUserParamsDTO) -> UserDTO:
        self._validate_params(user_dto=user_dto)
        user_dto = self.user_storage.create_users(user_dtos=[user_dto])
        return user_dto[0]

    def _validate_params(self, user_dto:CreateUserParamsDTO):
        if not user_dto.name:
            raise FullNameCanNotBeEmpty()

        mobile_number = self.validate_and_adjust_mobile_number(mobile_number=user_dto.mobile_number)
        user_dto.mobile_number = mobile_number

        pan_number = self.validate_and_adjust_pan_number(pan_number=user_dto.pan_number)
        user_dto.pan_number = pan_number

        if user_dto.manager_id:
            self.validate_manager_id(user_storage=self.user_storage, manager_id=user_dto.manager_id)
