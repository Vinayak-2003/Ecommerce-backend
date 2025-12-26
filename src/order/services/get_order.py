from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import status, HTTPException
from ..schema import Order
from ...address.schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def fetch_all_paginated_orders(token, page_no, per_page, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)
        total_orders_query = await db_session.execute(
            select(func.count())
            .select_from(Order)
            .where(Order.user_id == current_user_id))
        total_orders = total_orders_query.scalar_one_or_none()

        orders_for_page_query = await db_session.execute(
            select(Order)
            .where(Order.user_id == current_user_id)
            .offset((page_no-1) * per_page)
            .limit(per_page))
        orders_for_page = orders_for_page_query.scalars().all()

        total_pages = (total_orders + per_page - 1) // per_page

        response = {
            "orders": orders_for_page,
            "total_orders": total_orders,
            "page": page_no,
            "per page": per_page,
            "pages": total_pages
        }

        logger.info(f"Fetched paginated data for orders for page number {page_no}")
        return response
    except Exception as e:
        logger.error(f"An error raised while fetching orders: {str(e)}")
        await db_session.rollback()
        raise e


async def fetch_current_user_order_by_id(order_id, token, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)

        order_details_query = await db_session.execute(select(Order).where(
            Order.user_id == current_user_id,
            Order.order_id == order_id
        ))
        order_details = order_details_query.scalar_one_or_none()

        if order_details is None:
            logger.error("No order found")
            raise HTTPException(
                detail="No order found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        logger.info(f"Successfully fetched order of order id: {order_id}")
        return order_details
    except Exception as e:
        logger.error(f"An error occurred while fetching a order: {str(e)}")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    