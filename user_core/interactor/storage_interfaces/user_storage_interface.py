from abc import abstractmethod
from typing import List
from user_core.dtos import UserDTO, CreateUserParamsDTO, GetUsersParamsDTO, DeleteUserParamsDTO, UpdateUserParamsDTO


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

    @abstractmethod
    def filter_users(self, get_users_params:GetUsersParamsDTO) -> List[UserDTO]:
        pass

    @abstractmethod
    def delete_user(self, delete_user_params:DeleteUserParamsDTO) -> str:
        pass

    @abstractmethod
    def get_valid_user_ids(self, user_ids:List[str]) -> List[str]:
        pass

    @abstractmethod
    def update_user_manager_bulk(self, user_ids:List[str], manager_id:str) -> List[UserDTO]:
        pass

    @abstractmethod
    def update_user_data(self, user_id:str, update_user_params_dto:UpdateUserParamsDTO) -> UserDTO:
        pass