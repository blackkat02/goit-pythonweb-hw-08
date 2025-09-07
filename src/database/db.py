from ..config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager


username = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")
db_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")
port = config.get("DB", "DB_PORT")


DB_CONNECTION_URL = (
    f"postgresql+asyncpg://{username}:{password}@{domain}:{port}/{db_name}"
)


engine = create_async_engine(DB_CONNECTION_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def session_manager():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
