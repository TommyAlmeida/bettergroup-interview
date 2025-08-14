from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.models import User

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        
        return result.scalar_one_or_none()

    async def get_all_users(self) -> List[User]:
        result = await self.session.execute(select(User).order_by(User.email))
        
        return list(result.scalars().all())


    async def create_user(self, email: str, company_id: UUID):
        existing = await self.get_user_by_email(email)

        if existing:
            raise ValueError(f"User with email {email} already exists")
        
        user = User(email=email, company_id=company_id)

        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user
