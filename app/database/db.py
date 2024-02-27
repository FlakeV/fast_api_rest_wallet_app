from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.configuration.settings import settings

DATABASE_URL = settings.db_url

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
