from abc import abstractmethod
from typing import List
from user_core.dtos import UserDTO, CreateUserParamsDTO

class UserStorageInterface:
    @abstractmethod
    def create_users(self, user_dtos: List[CreateUserParamsDTO]) -> List[UserDTO]:
        pass

    @abstractmethod
    def is_user_id_exists(self,user_id:str) -> bool:
        pass

    @abstractmethod
    def is_user_active(self, user_id:str) -> bool:
        pass
