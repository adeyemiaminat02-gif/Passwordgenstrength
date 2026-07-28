"""Database interaction service abstraction."""

from sqlalchemy import select
from database import AsyncSessionLocal, UserPreference


class DatabaseService:
    """Service handling CRUD operations for user preferences."""

    @staticmethod
    async def get_user_preference(user_id: int) -> UserPreference:
        async with AsyncSessionLocal() as session:
            stmt = select(UserPreference).where(UserPreference.user_id == user_id)
            result = await session.execute(stmt)
            pref = result.scalar_one_or_none()

            if not pref:
                pref = UserPreference(user_id=user_id)
                session.add(pref)
                await session.commit()
                await session.refresh(pref)
            return pref

    @staticmethod
    async def update_user_preference(user_id: int, **kwargs) -> UserPreference:
        async with AsyncSessionLocal() as session:
            stmt = select(UserPreference).where(UserPreference.user_id == user_id)
            result = await session.execute(stmt)
            pref = result.scalar_one_or_none()

            if not pref:
                pref = UserPreference(user_id=user_id, **kwargs)
                session.add(pref)
            else:
                for key, value in kwargs.items():
                    if hasattr(pref, key):
                        setattr(pref, key, value)

            await session.commit()
            await session.refresh(pref)
            return pref
