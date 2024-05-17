import json
from django.http import HttpResponse

from user_core.dtos import UserDTO
from user_core.interactor.presenter_interfaces.presenter_interface import PresenterInterface

class Presenter(PresenterInterface):
    def get_response_for_create_user(self, user_dto: UserDTO) -> HttpResponse:
        response_dict = {
            "user_id":user_dto.user_id,
            "name": user_dto.name,
            "mobile_number": user_dto.mobile_number,
            "pan_number": user_dto.pan_number,
            "manager_id": user_dto.manager_id
        }
        response_json = json.dumps(response_dict)
        return HttpResponse(response_json, content_type='application/json', status=200)

    def get_error_http(self) -> HttpResponse:
        return HttpResponse('', content_type='application/json', status=400)