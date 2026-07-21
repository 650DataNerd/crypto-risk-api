import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.services.price_service import ingest_prices

logger = logging.getLogger(__name__)


async def run_price_ingestion():
    async with AsyncSessionLocal() as db:
        try:
            await ingest_prices(db)
            logger.info("Price ingestion completed successfully")
        except Exception as e:
            logger.error(f"Price ingestion failed: {e}")


async def start_worker(interval_seconds: int = 60):
    logger.info(f"Price worker started, interval: {interval_seconds}s")
    while True:
        await run_price_ingestion()
        await asyncio.sleep(interval_seconds)
