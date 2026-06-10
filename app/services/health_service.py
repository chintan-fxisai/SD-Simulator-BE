from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.health_repository import HealthRepository


class HealthService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = HealthRepository(db)

    async def check(self) -> dict[str, str]:
        await self.repository.check_database()
        return {"status": "ok", "database": "ok"}
