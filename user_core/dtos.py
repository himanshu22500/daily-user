from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    user_id : str
    name : str
    mobile_number: str
    pan_number: str
    manager_id: Optional[str]

@dataclass
class CreateUserParamsDTO:
    name: str
    mobile_number: str
    pan_number: str
    manager_id: Optional[str]