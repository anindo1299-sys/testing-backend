from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from core.auth import is_admin
from crud import crud_category
from schemas import CategoryCreate, CategoryPublic


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryPublic,  dependencies=[Depends(is_admin())])
async def create_category(category_data: CategoryCreate,
                           session: AsyncSession = Depends(get_session)):
    new_category = await crud_category.create_category(category_data=category_data, session=session)
    return new_category

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoryPublic])
async def get_all_category(session:AsyncSession = Depends(get_session)):
    all_category = await crud_category.get_all_category(session=session)
    return all_category

@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryPublic)
async def get_category_by_id(category_id: int,
                             session:AsyncSession = Depends(get_session)):
    category_by_id = await crud_category.get_category_by_id(category_id=category_id, session=session)
    if not category_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with the id of {category_id} does not exist")
    return category_by_id