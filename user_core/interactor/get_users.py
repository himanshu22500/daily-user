from typing import List

from django.http import HttpResponse

from user_core.dtos import GetUsersParamsDTO, UserDTO
from user_core.exceptions.expections import InvalidUserIds, ManagerDoesNotExists, InvalidManagerId, DeactivatedManager, \
    InvalidMobileNumber, MobileNumberAlreadyExists
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.interactor.validation_mixin import ValidationMixin


class GetUsersInteractor(ValidationMixin):
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage


    def get_users_wrapper(self, get_users_params:GetUsersParamsDTO, presenter:PresenterInterface) -> HttpResponse:
        try:
            user_dtos = self.get_users(get_users_params=get_users_params)
        except InvalidUserIds as err:
            return presenter.get_invalid_user_id_http_error(user_ids=err.user_ids)
        except ManagerDoesNotExists as err:
            return presenter.get_manager_not_found_http_error(manager_id=err.manager_id)
        except InvalidManagerId as err:
            return presenter.get_manager_not_found_http_error(manager_id=err.manager_id)
        except DeactivatedManager as err:
            return presenter.get_deactivated_manager_id_http_error(manager_id=err.manager_id)
        except InvalidMobileNumber as err:
            return presenter.get_invalid_mobile_number_http_error(mobile_number=err.mobile_number)
        except MobileNumberAlreadyExists as err:
            return presenter.get_mobile_number_already_exists_http_error(mobile_number=err.mobile_number)
        else:
            return presenter.get_response_for_get_users(user_dtos=user_dtos)

    def get_users(self, get_users_params:GetUsersParamsDTO) -> List[UserDTO]:
        self._validate_params(get_users_params=get_users_params)

        user_dtos = self.user_storage.filter_users(get_users_params=get_users_params)
        return user_dtos

    def _validate_params(self, get_users_params:GetUsersParamsDTO):
        if get_users_params.manager_id:
            self.validate_manager_id(user_storage=self.user_storage, manager_id=get_users_params.manager_id)

        if get_users_params.user_id:
            self.validate_user_ids(user_storage=self.user_storage, user_ids=[get_users_params.user_id])

        if get_users_params.mobile_number:
            self.validate_and_adjust_mobile_number(user_storage=self.user_storage,mobile_number=get_users_params.mobile_number)
