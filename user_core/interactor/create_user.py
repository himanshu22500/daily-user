from typing import List

from django.http import HttpResponse

from user_core.dtos import UserDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface
class CreateUserInteractor:
    def __init__(self, user_storage:UserStorageInterface):
        self.user_storage = user_storage

    def create_user_wrapper(self, user_dtos:List[UserDTO], presenter:PresenterInterface) -> HttpResponse:
        pass

    def create_users(self, user_dtos: List[UserDTO]):
        pass