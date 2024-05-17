from abc import abstractmethod
from typing import List
from user_core.dtos import UserDTO, CreateUserParamsDTO

class UserStorageInterface:
    @abstractmethod
    def create_users(self, user_dtos: List[CreateUserParamsDTO]) -> List[UserDTO]:
        pass
