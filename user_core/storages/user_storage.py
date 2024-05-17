from typing import List

from django.core.exceptions import ObjectDoesNotExist

from user_core.dtos import UserDTO, CreateUserParamsDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.models import models
class UserStorage(UserStorageInterface):
    def create_users(self, user_dtos: List[CreateUserParamsDTO]) -> List[UserDTO]:
        user_objs = [
            models.User(
                name=dto.name,
                mobile_number=dto.mobile_number,
                pan_number=dto.pan_number,
            )
            for dto in user_dtos
        ]
        user_objs = models.User.objects.bulk_create(user_objs)

        return self._create_user_dto_list(user_objs=user_objs)

    @staticmethod
    def _create_user_dto_list(user_objs):
        return [
            UserDTO(
                user_id=str(user_obj.id),
                name=user_obj.name,
                mobile_number=user_obj.mobile_number,
                pan_number=user_obj.pan_number,
                manager_id=user_obj.manager_id.id if user_obj.manager_id else None,
            )
            for user_obj in user_objs
        ]

    def is_user_id_exists(self,user_id:str) -> bool:
        return models.User.objects.filter(id=user_id).exists()

    def is_user_active(self, user_id: str) -> bool:
        try:
            user_obj = models.User.objects.get(id=user_id)
            return user_obj.is_active
        except ObjectDoesNotExist:
            return False