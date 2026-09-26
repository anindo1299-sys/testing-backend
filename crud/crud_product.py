from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import Product, Review
from schemas import ProductCreate
from sqlalchemy.orm import selectinload


async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    exec_quary = (
        select(Product).where(
            Product.id == db_product.id).\
            options(selectinload(Product.review)).\
            options(selectinload(Product.category))
    )
    egar_load = await session.exec(exec_quary)
    return egar_load.one()

async def get_all_product(session: AsyncSession) -> list[Product]:
    statement = (
        select(Product).\
            options(selectinload(Product.review).selectinload(Review.user)).\
            options(selectinload(Product.category))
    )
    result = await session.exec(statement)
    return result.all()

async def get_product_by_id(product_id: int, session: AsyncSession) -> Product:
    statement = (
        select(Product).where(
            Product.id == product_id).\
            options(selectinload(Product.review).selectinload(Review.user)).\
            options(selectinload(Product.category))
    )
    result = await session.exec(statement)
    return result.one_or_none()

async def get_product_by_category(category_id: int, session: AsyncSession) -> list[Product]:
    statement = (
        select(Product).where(
            Product.category_id == category_id).\
            options(selectinload(Product.review).selectinload(Review.user)).\
            options(selectinload(Product.category))
    )
    result = await session.exec(statement)
    return result.all()

async def get_all_product_paginated(skip: int, limit: int, session: AsyncSession) -> list[Product]:
    statement = (
        select(Product)
        .options(selectinload(Product.review).selectinload(Review.user))
        .options(selectinload(Product.category))
        .offset(skip)
        .limit(limit)
    )
    result = await session.exec(statement)
    return result.all()

