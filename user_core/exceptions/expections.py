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
