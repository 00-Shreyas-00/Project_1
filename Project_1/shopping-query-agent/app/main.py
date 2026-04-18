# shopping-query-agent/app/main.py
from __future__ import annotations

from fastapi import FastAPI
from app.routers import search

app = FastAPI(title="Shopping Query Agent API")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Simple health check endpoint to verify API status.
    """
    return {"status": "ok"}


# Include the search router
app.include_router(search.router, prefix="/api/v1", tags=["search"])
