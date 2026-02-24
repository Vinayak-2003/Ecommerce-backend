"""
Service module for fetching order details for the authenticated user.
"""
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..schema import Order

logger = get_logger(__name__)


async def fetch_all_paginated_orders(
    token: str, page_no: int, per_page: int, db_session: AsyncSession
):
    """
    Retrieves a paginated list of all orders for the authenticated user.
    """
    try:
        current_user_id = await get_current_user_id(token)
        total_orders_query = await db_session.execute(
            select(func.count())
            .select_from(Order)
            .where(Order.user_id == current_user_id)
        )
        total_orders = total_orders_query.scalar_one()

        orders_for_page_query = await db_session.execute(
            select(Order)
            .where(Order.user_id == current_user_id)
            .offset((page_no - 1) * per_page)
            .limit(per_page)
        )
        orders_for_page = orders_for_page_query.scalars().all()

        total_pages = (total_orders + per_page - 1) // per_page

        response = {
            "items": orders_for_page,
            "total": total_orders,
            "page": page_no,
            "per_page": per_page,
            "pages": total_pages,
        }

        logger.info(f"Fetched paginated data for orders for page number {page_no}")
        return response
    except Exception:
        logger.exception("An error occurred while fetching paginated orders")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def fetch_current_user_order_by_id(order_id: str, token: str, db_session: AsyncSession):
    """
    Retrieves a specific order by its ID for the authenticated user.
    """
    try:
        current_user_id = await get_current_user_id(token)

        order_details_query = await db_session.execute(
            select(Order).where(
                Order.user_id == current_user_id, Order.order_id == order_id
            )
        )
        order_details = order_details_query.scalar_one_or_none()

        if order_details is None:
            logger.warning(f"Order ID {order_id} not found for user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        logger.info(f"Successfully fetched order {order_id}")
        return order_details
    except HTTPException:
        raise
    except Exception:
        logger.exception("An error occurred while fetching order details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
