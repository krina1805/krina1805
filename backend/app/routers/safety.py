from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings
from app.services.safety_service import is_unsafe_text

router = APIRouter(prefix="/safety", tags=["safety"])


class SafetyCheckRequest(BaseModel):
    query: str


@router.post("/check")
def check_query(payload: SafetyCheckRequest) -> dict[str, str | bool]:
    blocked = is_unsafe_text(payload.query)
    return {
        "safe": not blocked,
        "message": "Query accepted." if not blocked else settings.safety_block_message,
    }
