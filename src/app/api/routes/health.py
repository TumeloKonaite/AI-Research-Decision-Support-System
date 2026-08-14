from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.app.infrastructure.database import database_is_ready

router = APIRouter(tags=["Service"])


@router.get(
    "/health",
    summary="Check service readiness",
    description="Returns success only when the API can reach its PostgreSQL database.",
)
async def health_check() -> dict[str, str]:
    if not database_is_ready():
        raise HTTPException(
            status_code=503,
            detail={"status": "unavailable", "database": "unavailable"},
        )
    return {"status": "ok"}
