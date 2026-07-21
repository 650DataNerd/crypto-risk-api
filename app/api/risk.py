from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.risk_service import get_risk_metrics

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/{symbol}")
async def risk_metrics(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_risk_metrics(db=db, symbol=symbol.upper())
