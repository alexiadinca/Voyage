from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness check used by the frontend and deployment platform."""
    return {"status": "ok"}
