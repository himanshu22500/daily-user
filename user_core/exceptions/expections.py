from typing import List


class FullNameCanNotBeEmpty(Exception):
    pass

class InvalidMobileNumber(Exception):
    def __init__(self, mobile_number:str):
        self.mobile_number = mobile_number

class InvalidManagerId(Exception):
    def __init__(self, manager_id:str):
        self.manager_id = manager_id

class ManagerDoesNotExists(Exception):
    def __init__(self, manager_id:str):
        self.manager_id = manager_id

class DeactivatedManager(Exception):
    def __init__(self, manager_id:str):
        self.manager_id = manager_id

class NoMatchingUserFound(Exception):
    pass

class InvalidUserIds(Exception):
    def __init__(self, user_ids:List[str]):
        self.user_ids = user_ids

class InvalidParamsForBulkUpdate(Exception):
    def __init__(self, fields:List[str]):
        self.fields = fields

class MobileNumberAlreadyExists(Exception):
    def __init__(self, mobile_number:str):
        self.mobile_number = mobile_number


class PanNumberAlreadyExists(Exception):
    def __init__(self, pan_number:str):
        self.pan_number = pan_number
