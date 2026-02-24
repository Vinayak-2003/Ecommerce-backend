"""
User controller for the E-Commerce Backend.
Defines endpoints for managing user profiles, including fetching current user,
updating user details, and administrative actions like role updates and deletions.
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_db_session
from utilities.rbac import require_permission

from ..auth.controller import oauth2_scheme
from .model import UserOut, UserRoleUpdateAdmin, UserUpdate
from .services.current_user import fetch_current_user
from .services.delete_user import delete_user_by_email
from .services.get_user import get_user_by_email_controller
from .services.update_user import (update_current_user,
                                   update_user_role_by_admin)

user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# user Get
@user_router.get("/me", response_model=UserOut)
async def fetch_active_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Endpoint to fetch the details of the currently authenticated user.
    """
    return await fetch_current_user(token, db)


@user_router.get(
    "/fetch-user-by-email/{email}",
    response_model=UserOut,
    dependencies=[Depends(require_permission("view_user"))],
)
async def fetch_user_by_email(email: str, db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint to fetch user details by their email address.
    Requires 'view_user' permission.
    """
    return await get_user_by_email_controller(email, db)


# user update
@user_router.put("/update-me/")
async def update_current_user_details(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_update_details: UserUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Endpoint for the current user to update their own profile details.
    """
    return await update_current_user(token, user_update_details, db)


@user_router.put(
    "/update-user-role/{email}",
    dependencies=[Depends(require_permission("update_role"))],
)
async def update_user_role_details(
    email: str,
    user_role_update_details: UserRoleUpdateAdmin,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Endpoint for an administrator to update a user's role.
    Requires 'update_role' permission.
    """
    return await update_user_role_by_admin(email, user_role_update_details, db)


# Delete User
@user_router.delete("/delete-user-by-email/{email}")
async def delete_user(email: str, db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint to delete a user by their email address.
    """
    return await delete_user_by_email(email, db)
