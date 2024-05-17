from abc import abstractmethod
from typing import List

from django.http import HttpResponse
from user_core.dtos import UserDTO


class PresenterInterface:
    @abstractmethod
    def get_response_for_create_user(self, user_dto: UserDTO) -> HttpResponse:
        pass

    @abstractmethod
    def get_empty_full_name_http_error(self) -> HttpResponse:
        pass

    @abstractmethod
    def get_invalid_mobile_number_http_error(self, mobile_number:str) -> HttpResponse:
        pass

    @abstractmethod
    def get_manager_not_found_http_error(self, manager_id:str) -> HttpResponse:
        pass

    @abstractmethod
    def get_deactivated_manager_id_http_error(self, manager_id:str) -> HttpResponse:
        pass

    @abstractmethod
    def get_response_for_get_users(self, user_dtos:List[UserDTO]) -> HttpResponse:
        pass

    @abstractmethod
    def get_response_for_delete_user(self, user_id:str) -> HttpResponse:
        pass

    @abstractmethod
    def get_no_user_deleted_http_error(self) -> HttpResponse:
        pass

    @abstractmethod
    def get_response_for_update_user(self,user_dtos:List[UserDTO]) -> HttpResponse:
        pass