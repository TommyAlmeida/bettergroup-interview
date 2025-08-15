from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserResponse(UserBase):
    id: UUID
    company_id: UUID

    class Config:
        from_attributes = True
