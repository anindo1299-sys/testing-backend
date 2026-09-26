from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from model.models import Review
from schemas import ReviewCreate


async def create_review(review_data: ReviewCreate, user_id: int, session: AsyncSession) -> Review:
    review_dict = review_data.model_dump(exclude={"user_id"})
    db_review = Review(**review_dict, user_id=user_id)
    session.add(db_review)
    await session.commit()
    await session.refresh(db_review)
    exec_quary = (
            select(Review).where(
                Review.id == db_review.id).\
                options(selectinload(Review.user))
        )
    egar_load = await session.exec(exec_quary)
    return egar_load.one()

async def get_review_by_product(product_id: int, session: AsyncSession) -> list[Review]:
    statement = (
        select(Review).where(
            Review.product_id == product_id).\
            options(selectinload(Review.user))
    )
    result = await session.exec(statement)
    return result.all()