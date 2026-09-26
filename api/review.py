from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from crud import crud_review, crud_product, crud_user
from schemas import ReviewCreate, ReviewPublic
from core.db import get_session


router = APIRouter()

class GetReviewWithUser(ReviewCreate):
    user_id: int

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewPublic)
async def create_review(review_data: GetReviewWithUser,
                        session: AsyncSession = Depends(get_session)):
    product = await crud_product.get_product_by_id(product_id=review_data.product_id,
                                                   session=session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {review_data.product_id} not found")
    user = await crud_user.get_user_by_id(user_id=review_data.user_id, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {review_data.user_id} not found")
    new_review = await crud_review.create_review(review_data=review_data,
                                                 user_id=review_data.user_id,
                                                 session=session)
    return new_review

@router.post("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=list[ReviewPublic])
async def get_review_by_product(product_id: int,
                                session: AsyncSession = Depends(get_session)):
    review = await crud_review.get_review_by_product(product_id=product_id, session=session)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Review with the product id of {product_id} does not exist")
    return review