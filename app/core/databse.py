import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config.config import settings


#Database URL
DATABASE_URL = settings.construct_db_url()


# Initialize Base
Base = declarative_base()


# Create async engine for DB
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,                 # Logs SQL Queries, need to be false while in production
    pool_pre_ping=True,        # Check connection health before executing the query
    pool_size=5,               # Standard pool size
    max_overflow=10,           # Max extra connections allowed under heavy load
)


# Initialize the Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# Get Async Database session
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields a database session context. Automatically ensures the session 
    is safely closed after the calling controller/route finishes execution.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

