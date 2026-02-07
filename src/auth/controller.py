from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .model import TokenSchema, RefreshRequest
from database.base import get_db_session
from ..user.model import UserCreate
from .services.signup import create_user_signup
from .services.login import user_login_controller
from .services.refresh_token import create_refresh_access_token
from .services.logout import user_logout_controller

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

# Auth Routes
@auth_router.post("/signup")
async def new_user_signup(new_user_data: UserCreate,
                    db: AsyncSession = Depends(get_db_session)
                ):
    return await create_user_signup(new_user_data, db)

@auth_router.post("/login", response_model=TokenSchema)
async def user_login(user_details: Annotated[OAuth2PasswordRequestForm, Depends()],
               response: Response,
               db: AsyncSession = Depends(get_db_session),
            ):
    return await user_login_controller(user_details, response, db)

@auth_router.post("/logout")
async def user_logout(request: Request,
                     response: Response, 
                    db: AsyncSession = Depends(get_db_session)
                ):
    return await user_logout_controller(request, response, db)

@auth_router.post("/refresh-token", response_model=TokenSchema)
async def refresh_access_token(request : Request,
                               response: Response,
                        db: AsyncSession = Depends(get_db_session)
                    ):
    return await create_refresh_access_token(request, response, db)