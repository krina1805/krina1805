from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/status")
def auth_status() -> dict[str, str]:
    return {"status": "optional_auth_not_enabled"}
