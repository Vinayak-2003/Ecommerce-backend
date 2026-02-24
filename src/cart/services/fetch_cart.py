"""
Service module for fetching user shopping cart items with pagination.
"""
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..schemas import CartItem

logger = get_logger(__name__)


async def fetch_cart_current_user(
    page_no: int, per_page: int, token: str, db_session: AsyncSession
):
    """
    Fetches the shopping cart items for the authenticated user with pagination support.
    """
    try:
        current_user_id = await get_current_user_id(token)
        
        # Get total count of cart items for the user
        total_query = await db_session.execute(
            select(func.count())
            .select_from(CartItem)
            .where(CartItem.user_id == current_user_id)
        )
        total_items = total_query.scalar_one()

        total_pages = (total_items + per_page - 1) // per_page

        if total_items == 0:
            logger.info(f"Cart is empty for user {current_user_id}")
            return {
                "items": [],
                "total": 0,
                "page": page_no,
                "per_page": per_page,
                "pages": total_pages,
            }

        # Get paginated cart items for the user
        cart_page_query = await db_session.execute(
            select(CartItem)
            .where(CartItem.user_id == current_user_id)
            .offset((page_no - 1) * per_page)
            .limit(per_page)
        )
        cart_items = cart_page_query.scalars().all()

        response = {
            "items": cart_items,
            "total": total_items,
            "page": page_no,
            "per_page": per_page,
            "pages": total_pages,
        }

        logger.info(f"Fetched paginated cart for user {current_user_id}")
        return response
    except Exception:
        logger.exception("An error occurred while fetching cart details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
