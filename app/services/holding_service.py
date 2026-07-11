from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.holding_repository import HoldingRepository
from app.schemas.holding import HoldingCreate, HoldingResponse


async def create_holding(db: AsyncSession, portfolio_id: int, data: HoldingCreate) -> HoldingResponse:
    repo = HoldingRepository(db)
    holding = await repo.create(
        portfolio_id=portfolio_id,
        symbol=data.symbol,
        amount=data.amount,
    )
    return HoldingResponse.model_validate(holding)


async def get_holdings(db: AsyncSession, portfolio_id: int) -> list[HoldingResponse]:
    repo = HoldingRepository(db)
    holdings = await repo.get_all(portfolio_id=portfolio_id)
    return [HoldingResponse.model_validate(h) for h in holdings]
