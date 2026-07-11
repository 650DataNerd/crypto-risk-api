from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.portfolio import router as portfolio_router
from app.api.holdings import router as holdings_router

app = FastAPI(title="Crypto Risk API")

app.include_router(health_router)
app.include_router(portfolio_router)
app.include_router(holdings_router)
