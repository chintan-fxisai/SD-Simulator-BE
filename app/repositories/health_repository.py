from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def check_database(self) -> bool:
        await self.db.execute(text("SELECT 1"))
        return True
