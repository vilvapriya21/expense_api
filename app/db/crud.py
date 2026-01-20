from datetime import date

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import hash_password
from app.db import models
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.schemas.user import UserCreate


def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    """Create a new expense for a specific user."""
    logger.info("Creating new expense")

    expense_data = expense.model_dump()

    if expense_data.get("expense_date") is None:
        expense_data["expense_date"] = date.today()

    db_expense = models.Expense(**expense_data, user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses_for_user(db: Session, user_id: int):
    """Retrieve all expenses for a user."""
    return (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .all()
    )


def get_expense_for_user(db: Session, expense_id: int, user_id: int):
    """Retrieve a single expense belonging to a user."""
    return (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == user_id,
        )
        .first()
    )


def update_expense_for_user(
    db: Session,
    expense_id: int,
    expense: ExpenseUpdate,
    user_id: int,
):
    """Update an existing expense."""
    db_expense = get_expense_for_user(db, expense_id, user_id)
    if not db_expense:
        return None

    for key, value in expense.model_dump(exclude_unset=True).items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense_for_user(db: Session, expense_id: int, user_id: int):
    """Delete an expense."""
    db_expense = get_expense_for_user(db, expense_id, user_id)
    if not db_expense:
        return None

    db.delete(db_expense)
    db.commit()
    return db_expense


def get_user_by_username(db: Session, username: str):
    """Fetch a user by username."""
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )


def create_user(db: Session, user: UserCreate):
    """Create a new user with a hashed password."""
    hashed_pwd = hash_password(user.password)

    db_user = models.User(
        username=user.username,
        hashed_password=hashed_pwd,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user