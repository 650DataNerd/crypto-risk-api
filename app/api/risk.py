from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.risk_service import get_risk_metrics
from app.services.price_service import get_latest_price

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/prices/{symbol}")
async def latest_price(
    symbol: str,
    current_user: User = Depends(get_current_user),
):
    price = await get_latest_price(symbol.upper())
    if price is None:
        raise HTTPException(status_code=404, detail=f"No price data for {symbol.upper()}")
    return {"symbol": symbol.upper(), "price_usd": str(price)}


@router.get("/{symbol}")
async def risk_metrics(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_risk_metrics(db=db, symbol=symbol.upper())
