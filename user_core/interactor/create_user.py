from django.http import HttpResponse

from user_core.dtos import UserDTO, CreateUserParamsDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
from user_core.exceptions.expections import FullNameCanNotBeEmpty, InvalidMobileNumber, InvalidManagerId, \
    ManagerDoesNotExists, DeactivatedManager

from user_core.interactor.uuid_mixin import UUIDMixin


class CreateUserInteractor(UUIDMixin):
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

        mobile_number = self._validate_and_adjust_mobile_number(mobile_number=user_dto.mobile_number)
        user_dto.mobile_number = mobile_number

        pan_number = self._validate_and_adjust_pan_number(pan_number=user_dto.pan_number)
        user_dto.pan_number = pan_number

        if user_dto.manager_id:
            self._validate_manager_id(manager_id=user_dto.manager_id)

    @staticmethod
    def _validate_and_adjust_mobile_number(mobile_number:str):
        if mobile_number.startswith('0'):
            mobile_number = mobile_number[1:]
        elif mobile_number.startswith('+91'):
            mobile_number = mobile_number[3:]

        is_mobile_number_valid = True
        for num in mobile_number:
            if num not in "0123456789":
                is_mobile_number_valid = False
                break

        if not is_mobile_number_valid:
            raise InvalidMobileNumber('Invalid mobile number')
        else:
            return mobile_number

    def _validate_and_adjust_pan_number(self, pan_number:str):
        capitalized_pan_number = ""
        for letter in pan_number:
            if letter.isalpha() and letter.islower():
                capitalized_pan_number += letter.upper()
            else:
                capitalized_pan_number += letter

        return capitalized_pan_number

    def _validate_manager_id(self, manager_id:str):
        if not self.is_valid_uuid_v4(uuid_str=manager_id):
            raise InvalidManagerId(manager_id=manager_id)

        is_manager_exists = self.user_storage.is_user_id_exists(user_id=manager_id)
        if not is_manager_exists:
            raise ManagerDoesNotExists(manager_id=manager_id)

        is_manager_active = self.user_storage.is_user_active(user_id=manager_id)
        if not is_manager_active:
            raise DeactivatedManager(manager_id=manager_id)