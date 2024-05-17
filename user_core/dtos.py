from dataclasses import dataclass


@dataclass
class UserDTO:
    user_id : str
    name : str
    mobile_number: str
    pan_number: str
    manager_id: str