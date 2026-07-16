from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.services.portfolio_service import create_portfolio, get_portfolios

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("/", response_model=list[PortfolioResponse])
async def list_portfolios(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_portfolios(db=db, user_id=current_user.id)


@router.post("/", response_model=PortfolioResponse, status_code=201)
async def create_new_portfolio(
    data: PortfolioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_portfolio(db=db, user_id=current_user.id, data=data)
