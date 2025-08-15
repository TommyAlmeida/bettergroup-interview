from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        """
        Initialize the user service with a database session.

        Args:
            session: The async database session to use for all operations
        """

        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by their email address.

        Args:
            email: The email address to search for

        Returns:
            The user if found, otherwise None
        """

        result = await self.session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by their unique ID.

        Args:
            user_id: The unique identifier for the user

        Returns:
            The user if found, otherwise None
        """

        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_all_users(self) -> List[User]:
        """
        Get all users in the system, ordered alphabetically by email.

        Returns:
            A list of all users sorted by email address
        """

        result = await self.session.execute(select(User).order_by(User.email))

        return list(result.scalars().all())

    async def create_user(self, email: str, company_id: UUID):
        """
        Create a new user account.

        Args:
            email: The user's email address (must be unique)
            company_id: The ID of the company this user belongs to

        Returns:
            The newly created user object

        Raises:
            ValueError: If a user with this email already exists
        """

        existing = await self.get_user_by_email(email)

        if existing:
            raise ValueError(f"User with email {email} already exists")

        user = User(email=email, company_id=company_id)

        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user
