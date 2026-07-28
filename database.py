"""Database models and async session management."""

import os
from typing import AsyncGenerator
from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DATABASE_URL

# Ensure local data directory exists for SQLite
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite+aiosqlite:///", "")
    dir_path = os.path.dirname(db_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


class UserPreference(Base):
    """User settings persistence model (NO PASSWORDS OR SECRETS ARE STORED)."""

    __tablename__ = "user_preferences"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    length: Mapped[int] = mapped_column(Integer, default=16)
    use_uppercase: Mapped[bool] = mapped_column(Boolean, default=True)
    use_lowercase: Mapped[bool] = mapped_column(Boolean, default=True)
    use_numbers: Mapped[bool] = mapped_column(Boolean, default=True)
    use_symbols: Mapped[bool] = mapped_column(Boolean, default=True)
    exclude_similar: Mapped[bool] = mapped_column(Boolean, default=False)
    exclude_ambiguous: Mapped[bool] = mapped_column(Boolean, default=False)
    passphrase_words: Mapped[int] = mapped_column(Integer, default=4)
    passphrase_separator: Mapped[str] = mapped_column(String(5), default="-")
    language: Mapped[str] = mapped_column(String(10), default="en")
    theme: Mapped[str] = mapped_column(String(20), default="dark")


async def init_db() -> None:
    """Initialize database schemas asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency helper to yield async database sessions."""
    async with AsyncSessionLocal() as session:
        yield session
