from fastapi import APIRouter

from app.schemas.health_check_schema import HealthCheckResponse

router = APIRouter(prefix='/api/v1', tags=['health_check'])


@router.get('/')
async def get_health_check() -> HealthCheckResponse:
    return HealthCheckResponse()
