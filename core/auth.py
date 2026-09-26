from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from decouple import config
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt

from model.models import User
from schemas import TokenData
from .db import get_session
from .security import verify_password


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/auth/token")

async def get_user(db: AsyncSession, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def role_checker(roles: set[str] | list[str]):
    def check_role_dependency(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not authorized for this action."
            )
        return current_user
    return check_role_dependency

def is_admin():
    return role_checker({"admin"})

def is_customer():
    return role_checker({"customer"})