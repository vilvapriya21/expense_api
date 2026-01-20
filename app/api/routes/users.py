"""
User management routes.

Handles user registration and profile retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...core import security
from ...db import crud
from ...schemas.user import UserCreate, UserResponse
from ...dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.
    """
    existing_user = crud.get_user_by_username(
        db, user.username
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )
    return crud.create_user(db, user)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user=Depends(security.get_current_user),
):
    """
    Retrieve the currently authenticated user's profile.
    """
    return current_user