import json

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.services.safety_service import is_unsafe_text


class SafetyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        if not body:
            return await call_next(request)

        try:
            payload = json.loads(body)
            text = json.dumps(payload)
        except json.JSONDecodeError:
            text = body.decode("utf-8", errors="ignore")

        if is_unsafe_text(text):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "unsafe_query",
                    "message": settings.safety_block_message,
                },
            )

        return await call_next(request)
