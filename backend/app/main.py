import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.database import init_db
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.middleware.safety_middleware import SafetyMiddleware
from app.routers import auth, safety, symptoms, topics
from app.services.topic_service import bootstrap_topics

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(title=settings.app_name, version="1.0.0")
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


@app.on_event("startup")
def startup() -> None:
    init_db()
    bootstrap_topics()


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


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
            "disclaimer": "General health education only. Not medical diagnosis or treatment.",
        },
    )
