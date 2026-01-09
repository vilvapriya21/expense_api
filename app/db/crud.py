from sqlalchemy.orm import Session
from . import models
from ..schemas.expense import ExpenseCreate, ExpenseUpdate
from ..schemas.user import UserCreate
from ..core.security import hash_password
from datetime import date
from app.core.logger import logger
# ---------- Expenses ----------


def create_expense(db: Session, expense: ExpenseCreate):
    logger.info("Creating new expense")
    expense_data = expense.model_dump()

    # REAL-TIME BEHAVIOR: server controls the date
    if expense_data.get("expense_date") is None:
        expense_data["expense_date"] = date.today()

    db_expense = models.Expense(**expense_data)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session):
    return db.query(models.Expense).all()

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def update_expense(db: Session, expense_id: int, expense: ExpenseUpdate):
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return None

    for key, value in expense.model_dump(exclude_unset=True).items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return None
    db.delete(db_expense)
    db.commit()
    return db_expense


# ---------- Users ----------

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user