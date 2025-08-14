from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.features.projects.models import Project, ProjectMembership
from app.features.users.models import User


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, name: str, company_id: UUID) -> Project:
        project = Project(
            name=name,
            company_id=company_id
        )

        self.db.add(project)

        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def get_project_by_id(self, project_id: UUID) -> Optional[Project]:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
      
        return result.scalar_one_or_none()

    async def get_all_projects(self, company_id: Optional[UUID] = None) -> List[Project]:
        query = select(Project)

        if company_id:
            query = query.where(Project.company_id == company_id)
        query = query.order_by(Project.name)
        
        result = await self.db.execute(query)

        return list(result.scalars().all())

    async def get_project_members(self, project_id: UUID) -> List[User]:
        result = await self.db.execute(
            select(User)
            .join(ProjectMembership)
            .where(ProjectMembership.project_id == project_id)
            .order_by(User.email)
        )
        
        return list(result.scalars().all())

    async def add_user_to_project(self, project_id: UUID, user_id: UUID) -> Optional[ProjectMembership]:
        existing = await self.db.execute(
            select(ProjectMembership).where(
                and_(
                    ProjectMembership.project_id == project_id,
                    ProjectMembership.user_id == user_id
                )
            )
        )

        if existing.scalar_one_or_none():
            return None

        project_result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )

        project = project_result.scalar_one_or_none()

        if not project:
            return None

        user_result = await self.db.execute(
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

        self.db.add(membership)

        await self.db.commit()
        await self.db.refresh(membership)

        return membership

    async def remove_user_from_project(self, project_id: UUID, user_id: UUID) -> bool:
        result = await self.db.execute(
            delete(ProjectMembership).where(
                and_(
                    ProjectMembership.project_id == project_id,
                    ProjectMembership.user_id == user_id
                )
            )
        )

        await self.db.commit()
        
        return result.rowcount > 0