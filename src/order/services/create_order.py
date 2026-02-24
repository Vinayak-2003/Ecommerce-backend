"""
Service module for creating new orders for the authenticated user.
"""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...address.schema import Address
from ...products.schema import Products
from ...user.services.current_user import get_current_user_id
from ..schema import Order, OrderItem

logger = get_logger(__name__)


async def create_order_current_user(new_order, token, db_session: AsyncSession):
    """
    Creates a new order for the authenticated user based on their default address and cart items.
    Updates product stock levels accordingly.
    """
    try:
        current_user_id = await get_current_user_id(token)

        # fetch current used default address id
        default_address_query = await db_session.execute(
            select(Address).where(
                Address.user_id == current_user_id, Address.is_default == True
            )
        )
        default_address = default_address_query.scalar_one_or_none()

        if not default_address:
            logger.warning(f"No default address found for user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Default address not found !!",
            )
        logger.info(f"Using default address ID {default_address.address_id} for order")

        # managing new order and order items for db
        new_order_dict = new_order.model_dump()
        ordered_items = new_order_dict.get("items")

        # merging quantities of the same product
        merged_items_dict = {}
        for item in ordered_items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            merged_items_dict[product_id] = merged_items_dict.get(product_id, 0) + quantity

        total_amount = 0
        order_items_data = []

        for p_id, qty in merged_items_dict.items():
            product_query = await db_session.execute(
                select(Products).where(Products.product_id == p_id)
            )
            product = product_query.scalar_one_or_none()

            if product is None:
                logger.error(f"Product with ID {p_id} not found during order creation")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product with ID {p_id} not found",
                )

            if product.available_quantity < qty:
                logger.warning(
                    f"Insufficient stock for product {product.product_name}. Adjusting to {product.available_quantity}"
                )
                qty = product.available_quantity

            if qty <= 0:
                continue

            total_product_price = product.price * qty
            total_amount += total_product_price

            # deduct stock quantity
            product.available_quantity -= qty

            # create order item object
            order_item = OrderItem(
                product_id=p_id,
                product_name=product.product_name,
                price_at_purchase=product.price,
                quantity=qty,
                total_price=total_product_price,
            )

            order_items_data.append(order_item)

        if not order_items_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid items to order (e.g. out of stock)"
            )

        # create order object
        new_order_entry = Order(
            user_id=current_user_id,
            shipping_address_id=default_address.address_id,
            payment_method=new_order.payment_method,
            total_items=len(order_items_data),
            total_amount=total_amount,
        )

        db_session.add(new_order_entry)
        await db_session.flush()  # generate order_id

        # attach order_id in order item object
        for item in order_items_data:
            item.order_id = new_order_entry.order_id
            db_session.add(item)

        await db_session.commit()
        await db_session.refresh(new_order_entry)
        logger.info(f"New order {new_order_entry.order_id} created successfully")
        return new_order_entry
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred while creating a new order")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
