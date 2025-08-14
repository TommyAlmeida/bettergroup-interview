from sqlalchemy import func, select
from app.features.analytics.schema import AnalyticsResponse
from app.features.companies.models import Company
from app.features.projects.models import Project, ProjectMembership
from app.features.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # In a real world application i would put this into a tdbms
    async def get_platform_analytics(self) -> AnalyticsResponse:
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
        result = await self.db.execute(select(func.count(model.id)))

        return result.scalar_one()
    
    async def _get_avg_users_per_company(self) -> float:
        result = await self.db.execute(
            select(func.avg(func.count(User.id)))
            .select_from(User)
            .group_by(User.company_id)
        )

        avg = result.scalar()

        return float(avg) if avg else 0.0

    async def _get_avg_projects_per_company(self) -> float:
        result = await self.db.execute(
            select(func.avg(func.count(Project.id)))
            .select_from(Project)
            .group_by(Project.company_id)
        )

        avg = result.scalar()

        return float(avg) if avg else 0.0

    async def _get_avg_members_per_project(self) -> float:
        result = await self.db.execute(
            select(func.avg(func.count(ProjectMembership.id)))
            .select_from(ProjectMembership)
            .group_by(ProjectMembership.project_id)
        )

        avg = result.scalar()

        return float(avg) if avg else 0.0