from uuid import UUID
from typing import List

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    company_id: UUID

class UserResponse(UserBase):
    id: UUID
    company_id: UUID
    
    class Config:
        from_attributes = True

class UserWithCompany(UserResponse):
    company_name: str
    company_domain: str

class UserWithProjects(UserWithCompany):
    projects: List[dict]
