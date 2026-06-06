from fastapi import APIRouter, status

from backend._constants import API_PREFIX_DUMMY

router = APIRouter(tags=["dummy"], prefix=API_PREFIX_DUMMY)


@router.get(
    "",
    summary="This is a dummy endpoint",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
    operation_id="dummy",
)
def dummy() -> list[str]:
    return ["REQUESTED", "PENDING"]
