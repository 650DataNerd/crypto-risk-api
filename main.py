from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.portfolio import router as portfolio_router
from app.api.holdings import router as holdings_router

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Crypto Risk API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(holdings_router)
