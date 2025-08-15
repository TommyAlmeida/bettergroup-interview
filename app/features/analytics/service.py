from sqlalchemy import func, select
from app.features.analytics.schema import AnalyticsResponse
from app.features.companies.models import Company
from app.features.projects.models import Project, ProjectMembership
from app.features.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        """
        Initialize the analytics service with a database session.

        Args:
            session: The async database session to use for all operations
        """
        self.session = session

    # In a real-world application I would put this into a time series database
    # like Prometheus
    async def get_platform_analytics(self) -> AnalyticsResponse:
        """
        Generate platform analytics.

        The metrics include both raw counts and calculated averages.

        Returns:
            AnalyticsResponse containing all calculated metrics including:
            - Total counts for companies, users, projects, and memberships
            - Average users per company
            - Average projects per company
            - Average members per project
        """

        companies_count = await self._get_count(Company)
        users_count = await self._get_count(User)
        projects_count = await self._get_count(Project)
        memberships_count = await self._get_count(ProjectMembership)

        avg_users_per_company = await self._get_avg_users_per_company()
        avg_projects_per_company = await self._get_avg_projects_per_company()
        avg_members_per_project = await self._get_avg_members_per_project()

        return AnalyticsResponse(
            total_companies=companies_count,
            total_users=users_count,
            total_projects=projects_count,
            total_memberships=memberships_count,
            avg_users_per_company=avg_users_per_company,
            avg_projects_per_company=avg_projects_per_company,
            avg_members_per_project=avg_members_per_project
        )


    async def _get_count(self, model) -> int:
        """
        Get the total number of records for a given model.

        Args:
            model: The SQLAlchemy model class to count

        Returns:
            The total number of records for this model
        """

        result = await self.session.execute(select(func.count(model.id)))

        return result.scalar_one()

    async def _get_avg_users_per_company(self) -> float:
        """
        Calculate the average number of users per company.

        Returns:
            The average number of users per company, or 0.0 if no companies exist
        """

        subquery = (
            select(func.count(User.id).label('user_count'))
            .select_from(User)
            .group_by(User.company_id)
        ).subquery()

        result = await self.session.execute(
            select(func.avg(subquery.c.user_count))
        )

        avg = result.scalar()

        return float(avg) if avg else 0.0

    async def _get_avg_projects_per_company(self) -> float:
        """
        Calculate the average number of projects per company.

        Returns:
            The average number of projects per company, or 0.0 if no companies exist
        """

        subquery = (
            select(func.count(Project.id).label('project_count'))
            .select_from(Project)
            .group_by(Project.company_id)
        ).subquery()

        result = await self.session.execute(
            select(func.avg(subquery.c.project_count))
        )

        avg = result.scalar()

        return float(avg) if avg else 0.0

    async def _get_avg_members_per_project(self) -> float:
        """
        Calculate the average number of members per project.

        Returns:
            The average number of members per project, or 0.0 if no projects exist
        """

        subquery = (
            select(func.count(ProjectMembership.id).label('member_count'))
            .select_from(ProjectMembership)
            .group_by(ProjectMembership.project_id)
        ).subquery()

        result = await self.session.execute(
            select(func.avg(subquery.c.member_count))
        )

        avg = result.scalar()

        return float(avg) if avg else 0.0
