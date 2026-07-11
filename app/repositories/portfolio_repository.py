from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.portfolio import Portfolio


class PortfolioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int) -> list[Portfolio]:
        result = await self.db.execute(
            select(Portfolio).where(Portfolio.user_id == user_id)
        )
        return result.scalars().all()

    async def create(self, user_id: int, name: str) -> Portfolio:
        portfolio = Portfolio(user_id=user_id, name=name)
        self.db.add(portfolio)
        await self.db.commit()
        await self.db.refresh(portfolio)
        return portfolio


    async def get_by_id(self, portfolio_id: int, user_id: int):
        result = await self.db.execute(
            select(Portfolio).where(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
