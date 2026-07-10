from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse


async def create_portfolio(db: AsyncSession, user_id: int, data: PortfolioCreate) -> PortfolioResponse:
    repo = PortfolioRepository(db)
    portfolio = await repo.create(user_id=user_id, name=data.name)
    return PortfolioResponse.model_validate(portfolio)


async def get_portfolios(db: AsyncSession, user_id: int) -> list[PortfolioResponse]:
    repo = PortfolioRepository(db)
    portfolios = await repo.get_all(user_id=user_id)
    return [PortfolioResponse.model_validate(p) for p in portfolios]
