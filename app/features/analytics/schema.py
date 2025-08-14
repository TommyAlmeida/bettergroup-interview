from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total_companies: int
    total_users: int
    total_projects: int
    total_memberships: int
    avg_users_per_company: float
    avg_projects_per_company: float
    avg_members_per_project: float
