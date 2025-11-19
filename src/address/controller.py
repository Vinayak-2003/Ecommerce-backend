from fastapi import APIRouter, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session

from .model import AddressCreate, AddressOut, AddressUpdate
from ..user_auth.controller import oauth2_scheme

from .services.all_address_current_user import all_current_user_addresses
from .services.create_address_current_user import create_current_user_address
from .services.update_address_current_user import update_current_user_address
from .services.delete_address_current_user import delete_current_user_address

from database.base import get_db_session

address_route = APIRouter(
    prefix="/api/v1/address",
    tags=["Address"]
)

@address_route.get("/fetch-all-address/me", response_model=List[AddressOut])
def fetch_my_address(token: Annotated[str, Depends(oauth2_scheme)],
                      db: Session = Depends(get_db_session)
                    ):
    return all_current_user_addresses(token, db)

@address_route.post("/create-address/me", response_model=AddressOut)
def create_address(new_address: AddressCreate,
                    token: Annotated[str, Depends(oauth2_scheme)],
                    db: Session = Depends(get_db_session)):
    return create_current_user_address(new_address, token, db)

@address_route.put("/update-address/{address_id}", response_model=AddressOut)
def update_address(address_id: str,
                   update_address: AddressUpdate,
                    token: Annotated[str, Depends(oauth2_scheme)],
                    db: Session = Depends(get_db_session)):
    return update_current_user_address(address_id, update_address, token, db)

@address_route.delete("/delete-address/{address_id}")
def delete_address(address_id: str,
                    token: Annotated[str, Depends(oauth2_scheme)],
                    db: Session = Depends(get_db_session)):
    return delete_current_user_address(address_id, token, db)