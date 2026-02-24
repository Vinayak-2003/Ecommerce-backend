from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Pydantic model representing the authentication token response.
    """
    access_token: str
    token_type: str = "Bearer"


class RefreshRequest(BaseModel):
    """
    Pydantic model representing a token refresh request.
    """
    refresh_token: str
