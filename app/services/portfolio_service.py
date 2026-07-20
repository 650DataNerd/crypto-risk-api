import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.core.cache import get_cached, set_cached, delete_cached


def _cache_key(user_id: int) -> str:
    return f"portfolios:{user_id}"


async def get_portfolios(db: AsyncSession, user_id: int) -> list[PortfolioResponse]:
    key = _cache_key(user_id)

    cached = await get_cached(key)
    if cached:
        data = json.loads(cached)
        return [PortfolioResponse(**item) for item in data]

    repo = PortfolioRepository(db)
    portfolios = await repo.get_all(user_id=user_id)
    result = [PortfolioResponse.model_validate(p) for p in portfolios]

    await set_cached(key, json.dumps([r.model_dump() for r in result], default=str))
    return result


async def create_portfolio(db: AsyncSession, user_id: int, data: PortfolioCreate) -> PortfolioResponse:
    repo = PortfolioRepository(db)
    portfolio = await repo.create(user_id=user_id, name=data.name)
    result = PortfolioResponse.model_validate(portfolio)

    await delete_cached(_cache_key(user_id))
    return result
