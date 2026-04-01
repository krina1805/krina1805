"""Compatibility entrypoint.

Use `uvicorn app.main:app` for new modular FastAPI backend.
"""

from app.main import app

__all__ = ["app"]
