from typing import List

from user_core.dtos import UserDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.models import models
class UserStorage(UserStorageInterface):
    def create_users(self, user_dtos: List[UserDTO]):
        pass