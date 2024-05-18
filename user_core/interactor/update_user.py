from typing import List

from django.http import HttpResponse

from user_core.dtos import UpdateUserParamsDTO, UserDTO
from user_core.exceptions.expections import InvalidUserIds, InvalidParamsForBulkUpdate, ManagerDoesNotExists, \
    InvalidManagerId, DeactivatedManager, InvalidMobileNumber
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.constants.enums import UserDataField
from user_core.interactor.validation_mixin import ValidationMixin


class UpdateUserInteractor(ValidationMixin):
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage

    def update_user_wrapper(self, update_user_params_dto:UpdateUserParamsDTO, presenter:PresenterInterface) -> HttpResponse:
        try:
            user_dtos = self.update_user(update_user_params_dto=update_user_params_dto)
        except InvalidUserIds as err:
            return presenter.get_invalid_user_id_http_error(user_ids=err.user_ids)
        except InvalidParamsForBulkUpdate as err:
            return presenter.get_bulk_update_not_allowed_http_error(fields=err.fields)
        except ManagerDoesNotExists as err:
            return presenter.get_manager_not_found_http_error(manager_id=err.manager_id)
        except InvalidManagerId as err:
            return presenter.get_manager_not_found_http_error(manager_id=err.manager_id)
        except DeactivatedManager as err:
            return presenter.get_deactivated_manager_id_http_error(manager_id=err.manager_id)
        except InvalidMobileNumber as err:
            return presenter.get_invalid_mobile_number_http_error(mobile_number=err.mobile_number)
        else:
            return presenter.get_response_for_update_user(user_dtos=user_dtos)

    def update_user(self, update_user_params_dto:UpdateUserParamsDTO) -> List[UserDTO]:
        self.validate_update_params(update_user_params_dto=update_user_params_dto)
        more_then_one_user_id_given = len(update_user_params_dto.user_ids) > 1

        if more_then_one_user_id_given:
            user_dtos = self.user_storage.update_user_manager_bulk(
                user_ids=update_user_params_dto.user_ids,
                manager_id=update_user_params_dto.manager_id
            )
        else:
            user_dto = self.user_storage.update_user_data(
                user_id=update_user_params_dto.user_ids[0],
                update_user_params_dto=update_user_params_dto
            )
            user_dtos = [user_dto]

        return user_dtos


    def validate_update_params(self, update_user_params_dto:UpdateUserParamsDTO):
        self.validate_user_ids(user_ids=update_user_params_dto.user_ids)
        self.validate_bulk_update_case(update_user_params_dto=update_user_params_dto)

        if update_user_params_dto.manager_id:
            self.validate_manager_id(user_storage=self.user_storage,manager_id=update_user_params_dto.manager_id)

        if update_user_params_dto.mobile_number:
            self.validate_and_adjust_mobile_number(mobile_number=update_user_params_dto.mobile_number)

    def validate_user_ids(self, user_ids:List[str]):
        valid_user_ids = self.user_storage.get_valid_user_ids(user_ids=user_ids)
        invalid_user_ids = [
            user_id
            for user_id in user_ids
            if user_id not in  valid_user_ids
        ]

        if invalid_user_ids:
            raise InvalidUserIds(user_ids=invalid_user_ids)

    def validate_bulk_update_case(self, update_user_params_dto:UpdateUserParamsDTO):
        more_then_one_user_id_given = len(update_user_params_dto.user_ids) > 1

        if more_then_one_user_id_given:
            given_fields = self.get_given_update_user_fields(
                update_user_params_dto=update_user_params_dto
            )
            manager_id_in_params = update_user_params_dto.manager_id is not None

            is_bulk_update_allowed = len(given_fields) == 1 and manager_id_in_params

            if not is_bulk_update_allowed:
                raise InvalidParamsForBulkUpdate(fields=given_fields)

    def get_given_update_user_fields(self, update_user_params_dto:UpdateUserParamsDTO):
        given_update_user_fields = []

        if update_user_params_dto.mobile_number:
            given_update_user_fields.append(UserDataField.MOBILE_NUMBER.value)
        if update_user_params_dto.name:
            given_update_user_fields.append(UserDataField.NAME.value)
        if update_user_params_dto.pan_number:
            given_update_user_fields.append(UserDataField.PAN_NUMBER.value)
        if update_user_params_dto.manager_id:
            given_update_user_fields.append(UserDataField.MANAGER_ID.value)

        return given_update_user_fields