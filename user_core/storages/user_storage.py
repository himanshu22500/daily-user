from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist

from user_core.dtos import UserDTO, CreateUserParamsDTO, GetUsersParamsDTO, DeleteUserParamsDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.models import models
class UserStorage(UserStorageInterface):
    def create_users(self, user_dtos: List[CreateUserParamsDTO]) -> List[UserDTO]:
        user_objs = [
            models.User(
                name=dto.name,
                mobile_number=dto.mobile_number,
                pan_number=dto.pan_number,
                is_active=True,
                manager_id=self._get_manager_obj(user_id=dto.manager_id)
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
                manager_id=str(user_obj.manager_id.id) if user_obj.manager_id else None,
                is_active=user_obj.is_active,
                created_at=user_obj.created_at,
                updated_at=user_obj.updated_at
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

    @staticmethod
    def _get_manager_obj(user_id:Optional[str]):
        if not user_id:
            return None

        return models.User.objects.get(id=user_id)

    def filter_users(self, get_users_params:GetUsersParamsDTO) -> List[UserDTO]:
        if get_users_params.user_id:
            user_objs = models.User.objects.filter(id=get_users_params.user_id)
            return self._create_user_dto_list(user_objs=user_objs)

        if get_users_params.mobile_number:
            user_objs = models.User.objects.filter(mobile_number=get_users_params.mobile_number)
            return self._create_user_dto_list(user_objs=user_objs)


        if get_users_params.manager_id:
            manager_obj = self._get_manager_obj(user_id=get_users_params.manager_id)
            user_objs = models.User.objects.filter(manager_id=manager_obj.id)
            return self._create_user_dto_list(user_objs=user_objs)

        all_user_objs = models.User.objects.all()
        return self._create_user_dto_list(user_objs=all_user_objs)


    def delete_user(self, delete_user_params:DeleteUserParamsDTO) -> str:
        deleted_user_id = None

        if delete_user_params.user_id:
            models.User.objects.filter(id=delete_user_params.user_id).delete()
            deleted_user_id = delete_user_params.user_id

        if delete_user_params.mobile_number:
            user = models.User.objects.filter(mobile_number=delete_user_params.mobile_number).first()

            if user:
                deleted_user_id = str(user.id)
                user.delete()

        return deleted_user_id
