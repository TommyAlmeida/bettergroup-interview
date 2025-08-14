import logging
import os
import sys
from typing import List

import httpx
import asyncio

# In case python path its wrongfully set
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import get_settings
from app.core.database import get_session
from app.features.companies.service import CompanyService
from app.features.projects.service import ProjectService
from app.features.users.service import UserService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def extract_domain_and_company(email: str) -> tuple[str, str]:
    domain = email.split("@")[1]
    company_name = domain.split(".")[0].capitalize()

    return domain, company_name

async def fetch_emails() -> List[str]:
    settings = get_settings()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://challenges.bettergroup.io/bp_backend/v1/{settings.candidate_id}/users",
                headers={"X-API-Key": settings.api_key}
            )

            response.raise_for_status()
            data = response.json()

            return data.get("users", [])
        except httpx.HTTPError as e:
            print(f"Failed to fetch emails: {e}")

            return []


async def sync_companies_and_users(db, emails: List[str]):
    companies_cache = {}
    users_cache = {}

    companies_service = CompanyService(db)
    users_service = UserService(db)

    for email in emails:
        domain, company_name = extract_domain_and_company(email)

        if company_name not in companies_cache:
            company = await companies_service.get_company_by_name(company_name)

            if not company:
                company = await companies_service.create_company(company_name, domain)
                logger.info(f"Company created: {company_name}")

            companies_cache[company_name] = company
            users_cache[company_name] = []

        user = await users_service.create_user(email, companies_cache[company_name].id)
        users_cache[company_name].append(user)

        logger.info(f"User created: {email}")

    return companies_cache, users_cache

async def assign_projects(db, companies_cache, users_cache):
    projects_service = ProjectService(db)

    for company_name, company in companies_cache.items():
        project_names = [f"{company_name} Sample Project 1", f"{company_name} Sample Project 2"]

        projects = [
            await projects_service.create_project(name, company.id)
            for name in project_names
        ]

        for user in users_cache[company_name]:
            for project in projects:
                await projects_service.add_user_to_project(project.id, user.id)
                logger.info(f"Assigned {user.email} to project {project.name}")

async def main():
    emails = await fetch_emails()

    if not emails:
        logger.error("No emails fetched.")
        return
    
    async for db in get_session():
        companies_cache, users_cache = await sync_companies_and_users(db, emails)

        await assign_projects(db, companies_cache, users_cache)

if __name__ == "__main__":
    asyncio.run(main())
