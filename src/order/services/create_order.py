from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status, HTTPException

from ..schema import Order, OrderItem
from ...address.schema import Address
from ...products.schema import Products
from ...products.model import ProductUpdate
from ...products.services.update_product import update_product_controller
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def create_order_current_user(new_order, token, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)

        # fetch current used default address id
        default_address_id_current_user_query = await db_session.execute(select(Address).where(
            Address.user_id == current_user_id,
            Address.is_default == True
        ))
        default_address_id_current_user = default_address_id_current_user_query.scalar_one_or_none()

        if not default_address_id_current_user:
            logger.error(f"Does not found any default address")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Default address not found !!"
            )
        logger.info(f"defualt address ID is {default_address_id_current_user.address_id}")
        
        # manageing new order and order items for db
        new_order_dict = new_order.model_dump()
        ordered_items = new_order_dict.get("items")

        # merging quantities of the same quantity
        merged_items_dict = {}
        for items in ordered_items:
            product_id = items["product_id"]
            quantity = items["quantity"]

            merged_items_dict[product_id] = merged_items_dict.get(product_id, 0) + quantity

        total_amount = 0
        order_items_data = []

        for id, qty in merged_items_dict.items():
            product_data_query = await db_session.execute(select(Products).where(Products.product_id == id))
            product_data = product_data_query.scalar_one_or_none()

            if product_data is None:
                logger.error(f"Does not found product with product id - {id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Does not found product with product id - {id}"
                )

            if product_data.available_quantity < qty:
                logger.warning(f"Available quantity for product {product_data.product_name} is less than the ordered quantity !!")
                qty = product_data.available_quantity

            total_product_price = product_data.price * qty
            total_amount += total_product_price

            # deduct stock quantity
            product_data.available_quantity -= qty

            # create order item object without order_id
            order_items = OrderItem(
                product_id = id,
                product_name = product_data.product_name,
                price_at_purchase = product_data.price,
                quantity = qty,
                total_price = total_product_price
            )

            order_items_data.append(order_items)

        # create order object
        new_order_complete_dict = Order(
            user_id = current_user_id,
            shipping_address_id = default_address_id_current_user.address_id,
            payment_method = new_order.payment_method,
            total_items = len(merged_items_dict),
            total_amount = total_amount
        )

        db_session.add(new_order_complete_dict)
        await db_session.flush()              # generate order_id

        # attach order_id in order item object
        for order_item in order_items_data:
            order_item.order_id = new_order_complete_dict.order_id
            db_session.add(order_item)

        await db_session.commit()
        await db_session.refresh(new_order_complete_dict)
        logger.info("New order created successfully !!")
        return new_order_complete_dict
    except Exception as e:
        logger.error(f"An error occurred while creating a new order for {current_user_id}: {str(e)}")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

