from abc import abstractmethod
from django.http import HttpResponse
from user_core.dtos import UserDTO


class PresenterInterface:
    @abstractmethod
    def get_response_for_create_user(self, user_dto: UserDTO) -> HttpResponse:
        pass

    @abstractmethod
    def get_error_http(self) -> HttpResponse:
        pass