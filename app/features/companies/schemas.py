from typing import List
import uuid
from pydantic import BaseModel

from app.features.users.schemas import UserResponse


class CompanyBase(BaseModel):
    name: str
    domain: str


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: uuid.UUID


class CompanyWithUsersResponse(CompanyResponse):
    users: List[UserResponse]
