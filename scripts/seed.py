import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.holding import Holding


async def seed():
    async with AsyncSessionLocal() as db:
        # Check if already seeded
        from sqlalchemy import select
        existing = await db.execute(select(User).where(User.email == "test@example.com"))
        if existing.scalar_one_or_none():
            print("Database already seeded, skipping.")
            return

        # Create test user
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password="not-a-real-hash",
            is_active=True,
        )
        db.add(user)
        await db.flush()

        # Create portfolios
        btc_portfolio = Portfolio(user_id=user.id, name="BTC Portfolio")
        eth_portfolio = Portfolio(user_id=user.id, name="ETH Portfolio")
        db.add(btc_portfolio)
        db.add(eth_portfolio)
        await db.flush()

        # Create holdings
        db.add(Holding(portfolio_id=btc_portfolio.id, symbol="BTC", amount="0.5"))
        db.add(Holding(portfolio_id=eth_portfolio.id, symbol="ETH", amount="2.3"))

        await db.commit()
        print("Database seeded successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
