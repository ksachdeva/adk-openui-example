from fastapi import APIRouter, status
from pydantic import BaseModel

from backend._constants import API_PREFIX_HEALTH

router = APIRouter(tags=["health"], prefix=API_PREFIX_HEALTH)


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@router.get(
    "",
    summary="Performs a health check",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
    operation_id="health-check",
)
def health() -> HealthCheck:
    return HealthCheck(status="OK")
