from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any, Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.core.config import settings
from ..db import crud
from app.dependencies import get_db

# ---------------- OAuth2 Scheme ----------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---------------- Password Hashing ----------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password (truncate to 72 bytes for bcrypt)"""
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed value"""
    return pwd_context.verify(plain_password[:72], hashed_password)


# ---------------- JWT TOKEN ----------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate JWT token with expiry"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_access_token(token: str, db: Session) -> Any:
    """Verify JWT token and return the user"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise JWTError()
    except JWTError:
        raise JWTError("Could not validate credentials")

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise JWTError("Could not validate credentials")

    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return verify_access_token(token, db)