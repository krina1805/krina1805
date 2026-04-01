from contextlib import asynccontextmanager
from typing import AsyncIterator


@asynccontextmanager
async def lifespan_stub() -> AsyncIterator[None]:
    """Placeholder lifespan manager for future DB wiring.

    The current implementation uses static data so this keeps startup/shutdown hooks in place
    without forcing a database dependency.
    """

    yield
