from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UserDTO:
    user_id : str
    name : str
    mobile_number: str
    pan_number: str
    manager_id: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

@dataclass
class CreateUserParamsDTO:
    name: str
    mobile_number: str
    pan_number: str
    manager_id: Optional[str]


@dataclass
class GetUsersParamsDTO:
    user_id: str
    mobile_number: Optional[str]
    manager_id:Optional[str]