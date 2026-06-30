from app.core.config import APP_NAME, APP_VERSION


def get_health_status() -> dict:
    return {"status": "ok"}


def get_version_info() -> dict:
    return {"name": APP_NAME, "version": APP_VERSION}


def get_ping_status() -> dict:
    return {"pong": True}
