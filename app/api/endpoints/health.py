from fastapi import APIRouter

from app.api.dependencies.db import DbSession
from app.schemas.common import ApiResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get("", response_model=ApiResponse[dict[str, str]])
async def health_check(db: DbSession) -> ApiResponse[dict[str, str]]:
    service = HealthService(db)
    data = await service.check()
    return ApiResponse(message="Service is healthy", data=data)
