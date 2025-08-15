from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, and_
from typing import List, Optional

from app.features.projects.models import Project, ProjectMembership
from app.features.users.models import User


class ProjectService:
    def __init__(self, session: AsyncSession):
        """
        Initialize the project service with a database session.

        Args:
            session: The async database session to use for all operations
        """

        self.session = session

    async def create_project(self, name: str, company_id: UUID) -> Project:
        """
        Create a new project within a company.

        Projects are always associated with a specific company and
        can only have members from that same company

        Args:
            name: The name of the project
            company_id: The company that owns this project

        Returns:
            The newly created project
        """

        project = Project(
            name=name,
            company_id=company_id
        )

        self.session.add(project)

        await self.session.commit()
        await self.session.refresh(project)

        return project

    async def get_project_by_id(self, project_id: UUID) -> Optional[Project]:
        """
        Retrieve a project by its unique ID.

        Args:
            project_id: The unique identifier for the project

        Returns:
            The project if found, otherwise None
        """

        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )

        return result.scalar_one_or_none()

    async def get_all_projects(
            self,
            company_id: Optional[UUID] = None
    ) -> List[Project]:
        """
        Get projects, optionally filtered by company.

        When company_id is provided, it returns only projects belonging to that company.
        When company_id is None, it returns all projects across all companies.

        Results are ordered alphabetically by project name.

        Args:
            company_id: Optional company ID to filter projects by

        Returns:
            A list of projects sorted by name
        """

        query = select(Project)

        if company_id:
            query = query.where(Project.company_id == company_id)
        query = query.order_by(Project.name)

        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def get_project_members(self, project_id: UUID) -> List[User]:
        """
        Get all users who are members of a specific project.

        Args:
            project_id: The project to get members for

        Returns:
            A list of users who are members of this project, sorted by email
        """

        result = await self.session.execute(
            select(User)
            .join(ProjectMembership)
            .where(ProjectMembership.project_id == project_id)
            .order_by(User.email)
        )

        return list(result.scalars().all())

    async def add_user_to_project(
            self,
            project_id: UUID,
            user_id: UUID
    ) -> Optional[ProjectMembership]:
        """
        Add a user as a member of a project.

        This method includes several safety checks:
        - Prevents duplicate memberships
        - Ensures the project exists
        - Ensures the user exists and belongs to the same company as the project

        Args:
            project_id: The project to add the user to
            user_id: The user to add as a member

        Returns:
            The new membership record if successful, None if the operation
            failed due to validation issues or if membership already exists
        """

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

    async def remove_user_from_project(
            self, project_id: UUID, user_id: UUID
    ) -> bool:
        """
        Remove a user from a project.

        Args:
            project_id: The project to remove the user from
            user_id: The user to remove from the project

        Returns:
            True if a membership was actually removed, False if no membership existed
        """

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

    async def get_project_by_name_and_company(
            self, name: str, company_id: UUID
    ) -> Optional[Project]:
        result = await self.session.execute(
            select(Project).where(
                and_(
                    Project.name == name,
                    Project.company_id == company_id
                )
            )
        )

        return result.scalar_one_or_none()
