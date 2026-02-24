"""
Address controller for the E-Commerce Backend.
Handles management of user shipping addresses, including creation, retrieval,
updating, and deletion.
"""
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_db_session

from ..auth.controller import oauth2_scheme
from .model import AddressCreate, AddressOut, AddressUpdate
from .services.all_address_current_user import all_current_user_addresses
from .services.create_address_current_user import create_current_user_address
from .services.delete_address_current_user import delete_current_user_address
from .services.update_address_current_user import update_current_user_address

address_route = APIRouter(prefix="/api/v1/address", tags=["Address"])


@address_route.get("/fetch-all-address/me", response_model=List[AddressOut])
async def fetch_my_address(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Fetches all addresses for the authenticated user.
    """
    return await all_current_user_addresses(token, db)


@address_route.post("/create-address/me", response_model=AddressOut)
async def create_address(
    new_address: AddressCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Creates a new address for the authenticated user.
    """
    return await create_current_user_address(new_address, token, db)


@address_route.put("/update-address/{address_id}", response_model=AddressOut)
async def update_address(
    address_id: str,
    address_update: AddressUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Updates an existing address for the authenticated user.
    """
    return await update_current_user_address(address_id, address_update, token, db)


@address_route.delete("/delete-address/{address_id}")
async def delete_address(
    address_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Deletes a specific address for the authenticated user.
    """
    return await delete_current_user_address(address_id, token, db)
