import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int | None = None):
        super().__init__(app)
        self.limit = limit or settings.rate_limit_per_minute
        self.window = 60
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        bucket = self.hits[client_ip]

        while bucket and now - bucket[0] > self.window:
            bucket.popleft()

        if len(bucket) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"error": "rate_limited", "message": "Too many requests. Please try again shortly."},
            )

        bucket.append(now)
        return await call_next(request)
