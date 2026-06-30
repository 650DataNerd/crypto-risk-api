from fastapi import APIRouter
from app.services.health_service import get_health_status, get_version_info, get_ping_status

router = APIRouter()


@router.get("/health")
def health():
    return get_health_status()


@router.get("/version")
def version():
    return get_version_info()

@router.get("/ping")
def ping():
    return get_ping_status()

