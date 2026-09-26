from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import User
from schemas import UserCreate
from core.security import get_password_hash


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    hashed_pwd = get_password_hash(password=user_data.password)
    user_dict = user_data.model_dump()
    user_dict["password"] = hashed_pwd
    db_user = User(**user_dict)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    return result.one_or_none()

async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.one_or_none()