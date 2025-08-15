
from fastapi import Depends
from app.core.database import get_session
from app.features.companies.service import CompanyService
from app.features.projects.service import ProjectService
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.service import UserService


def get_project_service(
    session: AsyncSession = Depends(get_session),
) -> ProjectService:
    return ProjectService(session)


def get_company_service(session: AsyncSession = Depends(
        get_session)) -> CompanyService:
    return CompanyService(session)


def get_user_service(session: AsyncSession = Depends(
        get_session)) -> UserService:
    return UserService(session)
