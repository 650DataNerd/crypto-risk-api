from fastapi import APIRouter
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.services.portfolio_service import create_portfolio, get_portfolios

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("/", response_model=list[PortfolioResponse])
def list_portfolios():
    return get_portfolios()


@router.post("/", response_model=PortfolioResponse, status_code=201)
def create_new_portfolio(data: PortfolioCreate):
    return create_portfolio(data)
