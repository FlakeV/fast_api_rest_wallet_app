from sqlalchemy import select

from app.database.db import async_session
from app.database.models import User
from app.schemas.auth import UserAdd
from app.database.models.base import object_as_dict


class UserService:
    @staticmethod
    async def get_by_id(user_id: int):
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()

    @staticmethod
    async def create_user(user: UserAdd):
        new_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            phone=user.phone,
        )
        async with async_session() as session:
            session.add(new_user)
            await session.commit()
        print(new_user)
        return object_as_dict(new_user)
