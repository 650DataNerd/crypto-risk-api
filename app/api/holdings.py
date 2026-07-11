from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.holding import HoldingCreate, HoldingResponse
from app.services.holding_service import create_holding, get_holdings
from app.repositories.portfolio_repository import PortfolioRepository

router = APIRouter(prefix="/portfolios/{portfolio_id}/holdings", tags=["holdings"])


async def get_portfolio_or_404(portfolio_id: int, db: AsyncSession = Depends(get_db)):
    repo = PortfolioRepository(db)
    portfolio = await repo.get_by_id(portfolio_id=portfolio_id, user_id=1)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.get("/", response_model=list[HoldingResponse])
async def list_holdings(
    portfolio_id: int,
    db: AsyncSession = Depends(get_db),
    portfolio=Depends(get_portfolio_or_404),
):
    return await get_holdings(db=db, portfolio_id=portfolio_id)


@router.post("/", response_model=HoldingResponse, status_code=201)
async def create_new_holding(
    portfolio_id: int,
    data: HoldingCreate,
    db: AsyncSession = Depends(get_db),
    portfolio=Depends(get_portfolio_or_404),
):
    return await create_holding(db=db, portfolio_id=portfolio_id, data=data)
