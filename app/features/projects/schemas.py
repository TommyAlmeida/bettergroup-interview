from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.features.users.schemas import UserResponse


class ProjectBase(BaseModel):
    name: str
    company_id: UUID


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: UUID


class ProjectWithMembersResponse(ProjectResponse):
    members: List[UserResponse]


class ProjectMembershipBase(BaseModel):
    user_id: UUID


class ProjectMembershipCreate(ProjectMembershipBase):
    pass


class ProjectMembershipResponse(ProjectMembershipBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    company_id: UUID
