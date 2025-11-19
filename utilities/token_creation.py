from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Union, Any
from config import get_settings

settings = get_settings()

def create_access_token(subject: Union[dict, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_TIME)
    
    to_encode = {
        "user_id": subject.get("user_id"),
        "exp": expires_delta,
        "sub": subject.get("sub"), 
        "role": subject.get("role")
    }
    encoded_jwt = jwt.encode(claims=to_encode, key=settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[dict, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_TIME)
    
    to_encode = {
        "user_id": subject.get("user_id"),
        "exp": expires_delta,
        "sub": subject.get("sub"), 
        "role": subject.get("role")
    }
    encoded_jwt = jwt.encode(claims=to_encode, key=settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt