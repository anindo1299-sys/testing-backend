from fastapi import APIRouter, Depends, HTTPException, status
from model.models import Order
from core.db import get_session
from tasks import process_order
from schemas import OrderCreate, OrderResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

router = APIRouter()

@router.post("/place-order/", response_model=OrderResponse)
async def place_order(order: OrderCreate, db:AsyncSession = Depends(get_session)):
    new_order = Order(customer_name=order.customer_name, item=order.item)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    process_order.delay(new_order.id)
    return new_order

@router.get("/order-status/{order_id}", response_model=OrderResponse)
async def get_order_status(order_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.exec(select(Order).where(Order.id == order_id))
    order = result.first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order
