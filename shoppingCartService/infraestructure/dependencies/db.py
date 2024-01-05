from sqlalchemy.ext.asyncio import AsyncSession
from db.sessions import async_session


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()
