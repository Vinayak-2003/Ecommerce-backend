"""
Utility functions for creating and decoding JWT access and refresh tokens.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from uuid import uuid4

from jose import jwt

from config import get_settings

settings = get_settings()


def create_access_token(subject: Union[dict, Any], expires_delta: int = None) -> str:
    """
    Generates a new JWT access token with user details and expiration time.
    """
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_TIME
        )

    to_encode = {
        "user_id": subject.get("user_id"),
        "exp": expires_delta,
        "sub": subject.get("sub"),
        "token_type": "access",
        "role": subject.get("role"),
    }
    return jwt.encode(
        claims=to_encode,
        key=settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(subject: Union[dict, Any], expires_delta: int = None) -> str:
    """
    Generates a new JWT refresh token for session maintenance.
    """
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_TIME
        )

    to_encode = {
        "user_id": subject.get("user_id"),
        "exp": expires_delta,
        "sub": subject.get("sub"),
        "token_type": "refresh",
    }
    return jwt.encode(
        claims=to_encode,
        key=settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str):
    """
    Decodes a JWT token without verifying expiration for internal payload extraction.
    """
    return jwt.decode(
        token,
        settings.JWT_ACCESS_SECRET_KEY,
        algorithms=settings.ALGORITHM,
        options={"verify_exp": False},
    )


def create_new_refresh_token():
    """
    Generates a random UUID-based refresh token and its expiration metadata.
    """
    new_refresh_token = str(uuid4())
    # Create timezone-naive datetime for database compatibility
    expires_delta = datetime.now() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_TIME
    )

    return {"token": new_refresh_token, "expires_at": expires_delta}
