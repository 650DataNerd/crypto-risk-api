from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.holding import Holding
from decimal import Decimal


class HoldingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, portfolio_id: int) -> list[Holding]:
        result = await self.db.execute(
            select(Holding).where(Holding.portfolio_id == portfolio_id)
        )
        return result.scalars().all()

    async def create(self, portfolio_id: int, symbol: str, amount: Decimal) -> Holding:
        holding = Holding(portfolio_id=portfolio_id, symbol=symbol, amount=amount)
        self.db.add(holding)
        await self.db.commit()
        await self.db.refresh(holding)
        return holding
