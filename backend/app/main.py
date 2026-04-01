import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.middleware.safety_middleware import SafetyMiddleware
from app.routers import auth, safety, symptoms, topics

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SafetyMiddleware)

app.include_router(topics.router, prefix=settings.api_prefix)
app.include_router(symptoms.router, prefix=settings.api_prefix)
app.include_router(safety.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "disclaimer": "General health education only. Not medical diagnosis or treatment.",
    }
