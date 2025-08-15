from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.features.companies.models import Company
from app.features.users.models import User


class CompanyService:
    def __init__(self, session: AsyncSession):
        """
        Initialize the company service with a database session.

        Args:
            session: The async database session to use for all operations
        """

        self.session = session

    async def get_all_companies(self) -> List[Company]:
        """
        Retrieve all companies in the database.

        Returns:
            A list of all companies
        """

        result = await self.session.execute(select(Company))

        return list(result.scalars().all())

    async def get_company_by_id(self, company_id: UUID) -> Optional[Company]:
        """
        Find a company by its unique ID.

        Args:
            company_id: The unique identifier for the company

        Returns:
            The company if found, otherwise None
        """

        result = await self.session.execute(
            select(Company).where(Company.id == company_id)
        )

        return result.scalar_one_or_none()

    async def get_company_by_name(
            self, company_name: str
    ) -> Optional[Company]:
        """
        Find a company by its name.

        Args:
            company_name: The name of the company to search for

        Returns:
            The company if found, otherwise None
        """

        result = await self.session.execute(
            select(Company).where(Company.name == company_name)
        )

        return result.scalar_one_or_none()

    async def get_company_by_domain(self, domain: str) -> Optional[Company]:
        """
        Find a company by its domain name.

        Args:
            domain: The domain to search for (e.g., "example.com")

        Returns:
            The company if found, otherwise None
        """

        result = await self.session.execute(
            select(Company).where(Company.domain == domain)
        )

        return result.scalar_one_or_none()

    async def get_company_users(self, company_id: UUID) -> List[User]:
        """
        Get all users that belong to a specific company.

        Args:
            company_id: The company to get users for

        Returns:
            A list of all users in the specified company
        """

        result = await self.session.execute(
            select(User).where(User.company_id == company_id)
        )

        return list(result.scalars().all())

    async def create_company(self, name: str, domain: str) -> Company:
        """
        Create a new company.

        Args:
            name: The name of the company
            domain: The company's domain (must be unique)

        Returns:
            The newly created company

        Raises:
            ValueError: If a company with this domain already exists
        """

        existing = await self.get_company_by_domain(domain)

        if existing:
            raise ValueError(f"Company with domain {domain} already exists")

        company = Company(name=name, domain=domain)

        self.session.add(company)

        await self.session.commit()
        await self.session.refresh(company)

        return company
