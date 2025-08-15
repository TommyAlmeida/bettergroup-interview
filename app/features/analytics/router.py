from fastapi import APIRouter, Depends

from app.core.database import get_session
from app.features.analytics.schema import AnalyticsResponse
from app.features.analytics.service import AnalyticsService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(db: AsyncSession = Depends(get_session)):
    service = AnalyticsService(db)

    analytics = await service.get_platform_analytics()

    return analytics
