from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_company_service, get_project_service
from app.features.companies.service import CompanyService
from app.features.projects.schemas import ProjectCreate, ProjectMembershipCreate, ProjectMembershipResponse, ProjectResponse, ProjectWithMembersResponse, ProjectWithMembersResponse
from app.features.projects.service import ProjectService
from app.features.users.schemas import UserResponse

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service),
    company_service: CompanyService = Depends(get_company_service)
):
    company = await company_service.get_company_by_id(project_data.company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    try:
        project = await project_service.create_project(project_data.name, project_data.company_id)

        return ProjectResponse.model_validate(project, from_attributes=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    company_id: Optional[UUID] = None,
    project_service: ProjectService = Depends(get_project_service),
):
    projects = await project_service.get_all_projects(company_id)

    return [
        ProjectResponse.model_validate(
            project,
            from_attributes=True
        ) for project in projects
    ]


@router.get("/projects/{project_id}",
            response_model=ProjectWithMembersResponse)
async def get_project_details(
    project_id: UUID,
    project_service: ProjectService = Depends(get_project_service),
):
    project = await project_service.get_project_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = await project_service.get_project_members(project_id)

    return ProjectWithMembersResponse(
        id=project.id,
        name=project.name,
        company_id=project.company_id,
        members=[
            UserResponse.model_validate(
                user,
                from_attributes=True
            ) for user in members
        ])


@router.post("/projects/{project_id}/members",
             response_model=ProjectMembershipResponse,
             status_code=201)
async def add_user_to_project(
    project_id: UUID,
    membership_data: ProjectMembershipCreate,
    project_service: ProjectService = Depends(get_project_service),
):
    membership = await project_service.add_user_to_project(project_id, membership_data.user_id)

    if not membership:
        raise HTTPException(
            status_code=400,
            detail="Could not add user to project. User may already be a member, or user/project doesn't exist."
        )

    return ProjectMembershipResponse.model_validate(
        membership, from_attributes=True
    )


@router.delete("/projects/{project_id}/members/{user_id}", status_code=204)
async def remove_user_from_project(
    project_id: UUID,
    user_id: UUID,
    project_service: ProjectService = Depends(get_project_service)
):
    success = await project_service.remove_user_from_project(project_id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Membership not found")

    return success


@router.get("/projects/{project_id}/members",
            response_model=List[UserResponse])
async def get_project_members(
    project_id: UUID,
    project_service: ProjectService = Depends(get_project_service)
):
    project = await project_service.get_project_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = await project_service.get_project_members(project_id)

    return [
        UserResponse.model_validate(
            user,
            from_attributes=True
        ) for user in members
    ]
