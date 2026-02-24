"""
Database models for authentication-related data.
Includes the RefreshToken model for managing user sessions.
"""
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class RefreshToken(Base):
    """
    SQLAlchemy model for storing refresh tokens.
    """
    __tablename__ = "refresh_tokens"

    token = Column(String, primary_key=True, nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="refresh_tokens")
