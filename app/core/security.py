"""
Security utilities.

Handles password hashing, JWT creation, and user authentication.
"""

from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import crud
from app.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Password is truncated to 72 bytes due to bcrypt limits.
    """
    return pwd_context.hash(password[:72])


def verify_password(
    plain_password: str, hashed_password: str
) -> bool:
    """
    Verify a plaintext password against a hashed value.
    """
    return pwd_context.verify(
        plain_password[:72], hashed_password
    )


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def verify_access_token(
    token: str, db: Session
) -> Any:
    """
    Verify a JWT token and return the associated user.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        username = payload.get("sub")
        if username is None:
            raise JWTError()
    except JWTError:
        raise JWTError("Could not validate credentials")

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise JWTError("Could not validate credentials")

    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Dependency to retrieve the currently authenticated user.
    """
    return verify_access_token(token, db)