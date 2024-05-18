from typing import List, Optional
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from user_core.dtos import UserDTO, CreateUserParamsDTO, GetUsersParamsDTO, DeleteUserParamsDTO, UpdateUserParamsDTO
from user_core.interactor.storage_interfaces.user_storage_interface import UserStorageInterface
from user_core.models import models
class UserStorage(UserStorageInterface):
    def create_users(self, user_dtos: List[CreateUserParamsDTO]) -> List[UserDTO]:
        user_objs = [
            models.User(
                name=dto.name,
                mobile_number=dto.mobile_number,
                pan_number=dto.pan_number,
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

    @staticmethod
    def _create_user_dto(user_obj):
        return UserDTO(
                user_id=str(user_obj.id),
                name=user_obj.name,
                mobile_number=user_obj.mobile_number,
                pan_number=user_obj.pan_number,
                manager_id=str(user_obj.manager_id.id) if user_obj.manager_id else None,
                is_active=user_obj.is_active,
                created_at=user_obj.created_at,
                updated_at=user_obj.updated_at
            )

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

    def get_valid_user_ids(self, user_ids:List[str]) -> List[str]:
        valid_user_ids = models.User.objects.filter(id__in=user_ids).values_list('id', flat=True)
        return [str(user_id) for user_id in valid_user_ids]

    def update_user_manager_bulk(self, user_ids:List[str], manager_id:str) -> List[UserDTO]:
        manager_user_obj = self._get_manager_obj(user_id=manager_id)
        user_objs = models.User.objects.filter(id__in=user_ids)
        for user_obj in user_objs:
            user_obj.manager_id = manager_user_obj
            user_obj.updated_at = datetime.now()

        models.User.objects.bulk_update(user_objs, fields=["manager_id"])
        return self._create_user_dto_list(user_objs=user_objs)

    def update_user_data(self, user_id:str, update_user_params_dto:UpdateUserParamsDTO) -> UserDTO:
        user_obj = models.User.objects.get(id=user_id)

        if update_user_params_dto.name:
            user_obj.name = update_user_params_dto.name

        if update_user_params_dto.pan_number:
            user_obj.pan_number = update_user_params_dto.pan_number

        if update_user_params_dto.mobile_number:
            user_obj.mobile_number = update_user_params_dto.mobile_number

        if update_user_params_dto.manager_id:
            manager_user_obj = self._get_manager_obj(user_id=update_user_params_dto.manager_id)
            user_obj.manager_id = manager_user_obj

        user_obj.updated_at = datetime.now()
        user_obj.save()
        return self._create_user_dto(user_obj=user_obj)

    def user_exists_with_given_mobile_number(self, mobile_number:str) -> bool:
        return models.User.objects.filter(mobile_number=mobile_number).exists()

    def user_exists_with_given_pan_number(self, pan_number:str) -> bool:
        return models.User.objects.filter(pan_number=pan_number).exists()

