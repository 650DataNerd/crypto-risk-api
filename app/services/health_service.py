from app.core.config import settings

def get_health_status() -> dict:
    return {"status": "ok"}


def get_version_info() -> dict:
    return {"name": settings.app_name, "version": settings.app_version}


def get_ping_status() -> dict:
    return {"pong": True}
