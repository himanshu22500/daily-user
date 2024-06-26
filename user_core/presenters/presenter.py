import json
from typing import List

from django.http import HttpResponse

from user_core.dtos import UserDTO
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface

class Presenter(PresenterInterface):
    def get_response_for_create_user(self, user_dto: UserDTO) -> HttpResponse:
        response_dict = {
            "user_id":user_dto.user_id,
            "full_name": user_dto.name,
            "mob_num": user_dto.mobile_number,
            "pan_num": user_dto.pan_number,
            "manager_id": user_dto.manager_id
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=200)


    def get_empty_full_name_http_error(self) -> HttpResponse:
        response_dict = {
            "message" : "full name can not be empty"
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=400)


    def get_invalid_mobile_number_http_error(self, mobile_number:str) -> HttpResponse:
        response_dict = {
            "message" : "invalid mobile number",
            "mobile_number": mobile_number
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=400)

    def get_manager_not_found_http_error(self, manager_id:str) -> HttpResponse:
        response_dict = {
            "message" : "manager not found",
            "manager_id": manager_id
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)

    def get_deactivated_manager_id_http_error(self, manager_id:str) -> HttpResponse:
        response_dict = {
            "message" : "manager is deactivated",
            "manager_id": manager_id
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)

    def get_response_for_get_users(self, user_dtos:List[UserDTO]) -> HttpResponse:
        user_dicts = self._get_user_dicts(user_dtos=user_dtos)
        response_dict = {
            "users":user_dicts,
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=200)

    @staticmethod
    def _get_user_dicts(user_dtos:List[UserDTO]):
        return [
            {
                "user_id": dto.user_id,
                "full_name": dto.name,
                "mob_num": dto.mobile_number,
                "pan_num": dto.pan_number,
                "manager_id": dto.manager_id,
                "created_at": str(dto.created_at),
                "updated_at": str(dto.updated_at)
            }
            for dto in user_dtos
        ]

    def get_response_for_delete_user(self,user_id:str) -> HttpResponse:
        response_dict = {
            "message" : "user deleted",
            "user_id": user_id
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=200)

    def get_no_user_deleted_http_error(self) -> HttpResponse:
        response_dict = {
            "message": "no user found to delete"
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)

    def get_response_for_update_user(self,user_dtos:List[UserDTO]) -> HttpResponse:
        user_dicts = self._get_user_dicts(user_dtos=user_dtos)
        response_dict = {
            "message":"users updated successfully",
            "users": user_dicts
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=200)

    def get_invalid_user_id_http_error(self, user_ids:List[str]) -> HttpResponse:
        response_dict = {
            "message" : "invalid user_ids",
            "user_ids": user_ids
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)

    def get_bulk_update_not_allowed_http_error(self, fields:List[str]):
        response_dict = {
            "message" : "bulk update not allowed with given fields",
            "user_ids": fields
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)

    def get_mobile_number_already_exists_http_error(self, mobile_number:str):
        response_dict = {
            "message" : "mobile number already exists",
            "mob_num": mobile_number
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)

    def get_pan_number_already_exists_http_error(self, pan_number:str):
        response_dict = {
            "message" : "pan number already exists",
            "mob_num": pan_number
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)

    def get_invalid_pan_number_http_error(self, pan_number:str)-> HttpResponse:
        response_dict = {
            "message" : "invalid pan number",
            "pan_num": pan_number
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=404)