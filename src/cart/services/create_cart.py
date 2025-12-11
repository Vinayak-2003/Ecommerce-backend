from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger
from ...products.schema import Products
from ..schemas import CartItem
from ..models import CartItemCreate, CartItemOut

logger = get_logger(__name__)

def create_cart_current_user(create_cart_details: CartItemCreate, token: str, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)

        product_price = db_session.query(Products.price).filter(
            Products.product_id == create_cart_details.product_id
        ).scalar()
        print("+++++++++++++++++++++++", product_price)
        
        cart_item = db_session.query(CartItem).filter(
            CartItem.user_id == current_user_id,
            CartItem.product_id == create_cart_details.product_id
        ).one_or_none()

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
            db_session.flush()
            
            logger.info(f"Created a new cart item")
            print("_________________________", cart_item)

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

        print("------------------------")

        db_session.commit()
        db_session.refresh(cart_item)

        print("=====================")

        logger.info(f"Successfully added item in the cart for user {current_user_id}")
        return result_cart_item
    except Exception as e:
        logger.error(f"An error occurred while creating cart: {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating cart: {str(e)}"
        )
    
# def check_for_already_stored_cart(current_user_id, product_id, quantity, db_session):

#     cart_item = db_session.query(CartItem).filter(
#             CartItem.user_id == current_user_id,
#             CartItem.product_id == product_id
#         ).one_or_none()
    
#     if cart_item is not None:
#         stored_data = db_session.query(CartItem).filter(
#             CartItem.user_id == current_user_id,
#             CartItem.cart_item_id == cart_item.cart_id
#         ).one_or_none()

#         stored_quantity = stored_data.quantity
#         update_quantity = quantity
        
#         stored_quantity += update_quantity

#         db_session.commit()
#         db_session.refresh(stored_data)