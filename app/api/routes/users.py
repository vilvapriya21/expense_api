from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db import crud
from ...schemas.user import UserCreate, UserResponse
from ...dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    return crud.create_user(db, user)