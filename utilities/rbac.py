from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

settings = get_settings()

roles_permissions = {
    "admin": {"create_user", "delete_user", "update_user", "update_role", "view_user"},
    "distributor": {"create_product", "view_product", "edit_product"},
    "customer": {"view_data", "update_self"},
}

def get_current_user_role(token: str):
    decode_token = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
    current_role = decode_token.get("role")
    return current_role

def require_permission(required_permission: str):

    def permission_dependency(token: str = Depends(oauth2_scheme)):
        user_role = get_current_user_role(token)
        allowed_permission = roles_permissions.get(user_role, set())
        if require_permission not in allowed_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission {required_permission} not allowed for role {user_role}"
            )
        
    return permission_dependency
