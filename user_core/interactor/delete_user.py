from django.http import HttpResponse

from user_core.dtos import DeleteUserParamsDTO
from user_core.exceptions.expections import NoMatchingUserFound, InvalidMobileNumber, InvalidUserIds, \
    MobileNumberAlreadyExists
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.interactor.validation_mixin import ValidationMixin


class DeleteUserInteractor(ValidationMixin):
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage

    def delete_user_wrapper(self, delete_user_params_dto:DeleteUserParamsDTO, presenter:PresenterInterface) -> HttpResponse:
        try:
            user_id = self.delete_user(delete_user_params_dto=delete_user_params_dto)
        except InvalidUserIds as err:
            return presenter.get_invalid_user_id_http_error(user_ids=err.user_ids)
        except NoMatchingUserFound:
            return presenter.get_no_user_deleted_http_error()
        except InvalidMobileNumber as err:
            return presenter.get_invalid_mobile_number_http_error(mobile_number=err.mobile_number)
        except MobileNumberAlreadyExists as err:
            return presenter.get_mobile_number_already_exists_http_error(mobile_number=err.mobile_number)
        else:
            return presenter.get_response_for_delete_user(user_id=user_id)

    def delete_user(self, delete_user_params_dto:DeleteUserParamsDTO) -> str:
        self._validate_params(delete_user_params_dto=delete_user_params_dto)

        user_id = self.user_storage.delete_user(delete_user_params=delete_user_params_dto)
        if not user_id:
            raise NoMatchingUserFound()

        return user_id

    def _validate_params(self, delete_user_params_dto:DeleteUserParamsDTO):
        if delete_user_params_dto.user_id:
            self.validate_user_ids(user_storage=self.user_storage, user_ids=[delete_user_params_dto.user_id])

        if delete_user_params_dto.mobile_number:
            self._validate_and_adjust_mobile_number(mobile_number=delete_user_params_dto.mobile_number)

    def _validate_and_adjust_mobile_number(self, mobile_number:str):
        if mobile_number.startswith('0'):
            mobile_number = mobile_number[1:]
        elif mobile_number.startswith('+91'):
            mobile_number = mobile_number[3:]

        is_mobile_number_valid = len(mobile_number) == 10
        for num in mobile_number:
            if num not in "0123456789":
                is_mobile_number_valid = False
                break

        if not is_mobile_number_valid:
            raise InvalidMobileNumber('Invalid mobile number')

        return mobile_number