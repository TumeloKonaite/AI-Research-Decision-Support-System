from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.app.api.routes.admin import router as admin_router
from src.app.api.routes.health import router as health_router
from src.app.api.routes.public import router as public_router
from src.app.api.middleware.public_recommendations import (
    PublicRecommendationTimingMiddleware,
)
from src.app.core.dependencies import get_app_settings


def load_runtime_environment() -> None:
    """Load .env into os.environ for SDKs that do not use app settings."""
    repo_root = Path(__file__).resolve().parents[3]
    candidates = (Path.cwd() / ".env", repo_root / ".env")

    for env_file in candidates:
        if env_file.exists():
            load_dotenv(dotenv_path=env_file, override=False)
            return


def create_app() -> FastAPI:
    load_runtime_environment()
    settings = get_app_settings()
    app = FastAPI(
        title="FPL Technocrat API",
        description=(
            "Public Fantasy Premier League recommendations and authenticated "
            "administrative pipeline operations."
        ),
        openapi_tags=[
            {
                "name": "Service",
                "description": "Service identity and readiness endpoints.",
            },
            {
                "name": "Public recommendations",
                "description": "Read-only published recommendation snapshots.",
            },
            {
                "name": "Admin",
                "description": (
                    "Protected report and pipeline operations. Every endpoint "
                    "requires an administrator bearer token."
                ),
            },
        ],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(PublicRecommendationTimingMiddleware)

    @app.get(
        "/",
        tags=["Service"],
        summary="Identify the API service",
        description="Returns the stable service name for basic discovery.",
    )
    async def root() -> dict[str, str]:
        return {"message": "FPL Technocrat API"}

    app.include_router(health_router)
    app.include_router(public_router)
    app.include_router(admin_router)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
