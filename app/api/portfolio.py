from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.services.portfolio_service import create_portfolio, get_portfolios

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("/", response_model=list[PortfolioResponse])
async def list_portfolios(db: AsyncSession = Depends(get_db)):
    return await get_portfolios(db=db, user_id=1)


@router.post("/", response_model=PortfolioResponse, status_code=201)
async def create_new_portfolio(data: PortfolioCreate, db: AsyncSession = Depends(get_db)):
    return await create_portfolio(db=db, user_id=1, data=data)
