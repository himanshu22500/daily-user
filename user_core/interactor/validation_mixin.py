from user_core.exceptions.expections import InvalidManagerId, ManagerDoesNotExists, DeactivatedManager, \
    InvalidMobileNumber
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
import uuid


class ValidationMixin:
    def validate_manager_id(self,user_storage:UserStorageInterface, manager_id:str):
        if not self.is_valid_uuid_v4(uuid_str=manager_id):
            raise InvalidManagerId(manager_id=manager_id)

        is_manager_exists = user_storage.is_user_id_exists(user_id=manager_id)
        if not is_manager_exists:
            raise ManagerDoesNotExists(manager_id=manager_id)

        is_manager_active = user_storage.is_user_active(user_id=manager_id)
        if not is_manager_active:
            raise DeactivatedManager(manager_id=manager_id)

    @staticmethod
    def validate_and_adjust_pan_number(pan_number:str):
        capitalized_pan_number = ""
        for letter in pan_number:
            if letter.isalpha() and letter.islower():
                capitalized_pan_number += letter.upper()
            else:
                capitalized_pan_number += letter

        return capitalized_pan_number

    @staticmethod
    def validate_and_adjust_mobile_number(mobile_number:str):
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
        else:
            return mobile_number

    @staticmethod
    def is_valid_uuid_v4(uuid_str):
        try:
            uuid_obj = uuid.UUID(uuid_str, version=4)
        except ValueError:
            return False
        return True