import time
from sqlalchemy import create_engine
from sqlmodel import Session, select

from core.config import get_settings
from model.models import Order
from worker import celery_app

Setting = get_settings()

engine = create_engine(Setting.DATABASE_SYNC_URL, echo=True)

STATUS = ["Packaging", "Shipping", "Delivered"]


def get_sync_session():
    with Session(engine) as session:
        yield session

@celery_app.task
def process_order(order_id: int):
    session = next(get_sync_session())
    try:
        order = session.exec(select(Order).where(Order.id == order_id)).first()
        if not order:
            return {"error": "Order not found"}

        for stage in STATUS:
            time.sleep(10)
            order.status = stage
            session.add(order)
            session.commit()
            session.refresh(order)

        return {"order_id": order.id, "final_status": order.status}
    finally:
        session.close()