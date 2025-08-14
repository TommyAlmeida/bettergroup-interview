import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.features.users.schemas import UserWithCompany

router = APIRouter()

@router.get("/", response_model=List[UserWithCompany])
async def list_users(
        company_id: Optional[uuid.UUID] = None,
        db: AsyncSession = Depends(get_session),
):
    print(company_id)