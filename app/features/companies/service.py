from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import uuid

from app.features.companies.models import Company
from app.features.users.models import User

class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_companies(self) -> List[Company]:
        result = await self.session.execute(select(Company))

        return list(result.scalars().all())

    async def get_company_by_id(self, company_id: uuid.UUID) -> Optional[Company]:
        result = await self.session.execute(
            select(Company).where(Company.id == company_id)
        )

        return result.scalar_one_or_none()

    async def get_company_by_name(self, company_name: str) -> Optional[Company]:
        result = await self.session.execute(
            select(Company).where(Company.name == company_name)
        )

        return result.scalar_one_or_none()

    async def get_company_by_domain(self, domain: str) -> Optional[Company]:
        result = await self.session.execute(
            select(Company).where(Company.domain == domain)
        )

        return result.scalar_one_or_none()

    async def get_company_users(self, company_id: uuid.UUID) -> List[User]:
        result = await self.session.execute(
            select(User).where(User.company_id == company_id)
        )

        return list(result.scalars().all())


    async def create_company(self, name: str, domain: str) -> Company:
        existing = await self.get_company_by_domain(domain)

        if existing:
            raise ValueError(f"Company with domain {domain} already exists")

        company = Company(name=name, domain=domain)

        self.session.add(company)

        await self.session.commit()
        await self.session.refresh(company)

        return company
