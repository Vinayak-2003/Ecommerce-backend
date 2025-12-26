from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger
from ...products.schema import Products
from ..schemas import CartItem
from ..models import CartItemCreate, CartItemOut

logger = get_logger(__name__)

async def create_cart_current_user(create_cart_details: CartItemCreate, token: str, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)

        product_price_query = await db_session.execute(select(Products.price).where(
            Products.product_id == create_cart_details.product_id
        ))
        product_price = product_price_query.scalar_one_or_none()
        
        cart_item_query = await db_session.execute(select(CartItem).where(
            CartItem.user_id == current_user_id,
            CartItem.product_id == create_cart_details.product_id
        ))
        cart_item = cart_item_query.scalar_one_or_none()

        total_product_amount = create_cart_details.quantity * product_price

        if cart_item is not None:
            logger.info(f"Product already exists in your {current_user_id} cart")
            
            cart_item.quantity += create_cart_details.quantity
            cart_item.total_quantity_amount = cart_item.quantity * product_price

            logger.info(f"Existed cart details fetched and updated")
        else:
            logger.info(f"Product does not exists in your {current_user_id} cart")
            cart_item = CartItem(
                product_id = create_cart_details.product_id,
                quantity = create_cart_details.quantity,
                user_id = current_user_id,
                product_amount = product_price,
                total_quantity_amount = total_product_amount
            )
            db_session.add(cart_item)
            await db_session.flush()
            
            logger.info(f"Created a new cart item")

        result_cart_item = CartItemOut(
            cart_item_id = cart_item.cart_item_id,
            product_id = create_cart_details.product_id,
            quantity = create_cart_details.quantity,
            user_id = current_user_id,
            product_amount = product_price,
            total_quantity_amount = total_product_amount,
            created_datetime = cart_item.created_datetime,
            last_updated_datetime = cart_item.last_updated_datetime
        )

        await db_session.commit()
        await db_session.refresh(cart_item)

        logger.info(f"Successfully added item in the cart for user {current_user_id}")
        return result_cart_item
    except Exception as e:
        logger.error(f"An error occurred while creating cart: {str(e)}")
        await db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating cart: {str(e)}"
        )
    