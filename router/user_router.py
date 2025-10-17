from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from models.user_model import (UserOut, 
                               UserCreate, 
                               UserUpdate, 
                               TokenSchema, 
                               UserLoginSchema, 
                               UserRoleUpdateAdmin
                            )
from database.base import get_db_session

from controllers.users.signup import create_user_signup
from controllers.users.login import user_login_controller
from controllers.users.get_user import get_user_by_email_controller
from controllers.users.current_user import fetch_current_user
from controllers.users.update_user import update_current_user, update_user_role_by_admin
from controllers.users.delete_user import delete_user_by_email

from utilities.rbac import require_permission

user_router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

# User Post - SignUp and Signin
@user_router.post("/signup")
def new_user_signup(new_user_data: UserCreate,
                    db: Session = Depends(get_db_session)
                ):
    return create_user_signup(new_user_data, db)

@user_router.post("/login", response_model=TokenSchema)
def user_login(user_details: Annotated[OAuth2PasswordRequestForm, Depends()],
               db: Session = Depends(get_db_session)
            ):
    return user_login_controller(user_details, db)

# user Get
@user_router.get("/me", response_model=UserOut)
def fetch_active_user(token: Annotated[str, Depends(oauth2_scheme)],
                      db: Session = Depends(get_db_session)
                    ):
    return fetch_current_user(token, db)

@user_router.get("/fetch-user-by-email/{email}",
                 response_model=UserOut, 
                 dependencies=[Depends(require_permission("view_user"))]
                )
def fetch_user_by_email(email: str,
                        db: Session = Depends(get_db_session)
                    ):
    return get_user_by_email_controller(email, db)

# user update
@user_router.put("/update-me/")
def update_current_user_details(token: Annotated[str, Depends(oauth2_scheme)],
                        user_update_details: UserUpdate,
                        db: Session = Depends(get_db_session)
                    ):
    return update_current_user(token, user_update_details, db)

@user_router.put("/update-user-role/{email}", 
                 dependencies=[Depends(require_permission("update_role"))]
                )
def update_user_role_details(email: str,
                        user_role_update_details: UserRoleUpdateAdmin,
                        db: Session = Depends(get_db_session)
                    ):
    return update_user_role_by_admin(email, user_role_update_details, db)

# Delete User
@user_router.delete("/delete-user-by-email/{email}")
def delete_user(email: str,
                db: Session = Depends(get_db_session)
            ):
    return delete_user_by_email(email, db)