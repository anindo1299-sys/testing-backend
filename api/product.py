from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

from core.db import get_session
from crud import crud_product
from core.auth import get_current_user, is_admin
from schemas import ProductCreate, ProductPublic
from model.models import User


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductPublic, dependencies=[Depends(is_admin())])
async def create_new_product(product_data: ProductCreate,
                              session:AsyncSession = Depends(get_session)):
    new_product = await crud_product.create_product(product_data=product_data, session=session)
    return new_product

@router.get("/", response_model=list[ProductPublic])
async def get_all_product(
    session: AsyncSession = Depends(get_session),
    *, _: Annotated[User, Depends(get_current_user)]
):
    products = await crud_product.get_all_product(session=session)
    return products

@router.get("/paginated", response_model=list[ProductPublic])
async def get_paginated_product(
    skip: int = Query( 0, ge= 0, description="How many items to skip from the begining."),
    limit: int = Query( 10, ge= 0, le= 100, description="The maximum number of items to return per page."),
    session: AsyncSession = Depends(get_session)
):
    products = await crud_product.get_all_product_paginated(
        skip=skip, limit=limit, session=session
    )
    return products

@router.get("/category/{category_id}", response_model=list[ProductPublic])
async def get_product_by_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    *, _: Annotated[User, Depends(get_current_user)]
):
    products = await crud_product.get_product_by_category(category_id=category_id, session=session)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Product with category id of {category_id} not available")
    return products

@router.get("/{product_id}", response_model=ProductPublic)
async def get_product_details(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await crud_product.get_product_by_id(product_id=product_id, session=session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Product with id {product_id} not available")
    return product