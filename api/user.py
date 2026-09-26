from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

from crud import crud_user
from schemas import UserCreate, UserPublic, UserBase
from model.models import User
from core.db import get_session
from schemas import Token, UserPublic
from core.auth import get_current_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(user_data: UserCreate,
                      session:AsyncSession = Depends(get_session)):
    user = await crud_user.get_user_by_username(username=user_data.username, session=session)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"User with the username: {user_data.username} already exists")
    new_user = await crud_user.create_user(user_data=user_data, session=session)
    return new_user

@router.post("/auth/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: AsyncSession = Depends(get_session)) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def get_user_by_id(user_id: int, session:AsyncSession = Depends(get_session)):
    user = await crud_user.get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user by the id of {user_id} not found")
    return user

@router.get("/username/{username}", status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_session)):
    user = await crud_user.get_user_by_username(username=username, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User by the usename of {username} is not found")
    return user
