"""
Expense management routes.

Provides CRUD operations for user-specific expenses.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db import crud
from ...schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)
from ...dependencies import get_db
from ...core import security

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def get_current_user(
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Retrieve the currently authenticated user from JWT token.

    Args:
        token (str): JWT access token.
        db (Session): Database session.

    Returns:
        User: Authenticated user.
    """
    return security.verify_access_token(token, db)


@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a new expense for the authenticated user.
    """
    return crud.create_expense(db, expense, current_user.id)


@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve all expenses for the authenticated user.
    """
    return crud.get_expenses_for_user(db, current_user.id)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve a specific expense by ID.
    """
    expense = crud.get_expense_for_user(
        db, expense_id, current_user.id
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update an existing expense.
    """
    updated = crud.update_expense_for_user(
        db, expense_id, expense, current_user.id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated


@router.delete("/{expense_id}", status_code=204)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete an expense by ID.
    """
    deleted = crud.delete_expense_for_user(
        db, expense_id, current_user.id
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")