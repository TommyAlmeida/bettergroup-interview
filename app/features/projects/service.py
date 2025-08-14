from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, and_
from typing import List, Optional

from app.features.projects.models import Project, ProjectMembership
from app.features.users.models import User


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_project(self, name: str, company_id: UUID) -> Project:
        project = Project(
            name=name,
            company_id=company_id
        )

        self.session.add(project)

        await self.session.commit()
        await self.session.refresh(project)

        return project

    async def get_project_by_id(self, project_id: UUID) -> Optional[Project]:
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
      
        return result.scalar_one_or_none()

    async def get_all_projects(self, company_id: Optional[UUID] = None) -> List[Project]:
        query = select(Project)

        if company_id:
            query = query.where(Project.company_id == company_id)
        query = query.order_by(Project.name)
        
        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def get_project_members(self, project_id: UUID) -> List[User]:
        result = await self.session.execute(
            select(User)
            .join(ProjectMembership)
            .where(ProjectMembership.project_id == project_id)
            .order_by(User.email)
        )
        
        return list(result.scalars().all())

    async def add_user_to_project(self, project_id: UUID, user_id: UUID) -> Optional[ProjectMembership]:
        existing = await self.session.execute(
            select(ProjectMembership).where(
                and_(
                    ProjectMembership.project_id == project_id,
                    ProjectMembership.user_id == user_id
                )
            )
        )

        if existing.scalar_one_or_none():
            return None

        project_result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )

        project = project_result.scalar_one_or_none()

        if not project:
            return None

        user_result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        user = user_result.scalar_one_or_none()

        if user is None or user.company_id != project.company_id:
            return None

        membership = ProjectMembership(
            project_id=project_id,
            user_id=user_id,
            company_id=project.company_id
        )

        self.session.add(membership)

        await self.session.commit()
        await self.session.refresh(membership)

        return membership

    async def remove_user_from_project(self, project_id: UUID, user_id: UUID) -> bool:
        result = await self.session.execute(
            delete(ProjectMembership).where(
                and_(
                    ProjectMembership.project_id == project_id,
                    ProjectMembership.user_id == user_id
                )
            )
        )

        await self.session.commit()
        
        return result.rowcount > 0
    

    async def get_project_by_name_and_company(self, name: str, company_id: UUID) -> Optional[Project]:
        result = await self.session.execute(
            select(Project).where(
                and_(
                    Project.name == name,
                    Project.company_id == company_id
                )
            )
        )
        
        return result.scalar_one_or_none()