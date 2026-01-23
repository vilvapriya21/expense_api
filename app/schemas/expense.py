from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class ExpenseBase(BaseModel):
    amount: float = Field(
        ..., gt=0, description="Expense amount must be greater than zero"
    )
    category: str = Field(
        ..., min_length=1, max_length=50
    )
    description: Optional[str] = Field(
        None, max_length=255
    )
    expense_date: Optional[date] = None

    @field_validator("expense_date")
    @classmethod
    def validate_date(cls, value):
        if value and value > date.today():
            raise ValueError("Expense date cannot be in the future")
        return value


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    expense_date: Optional[date] = None

    @field_validator("expense_date")
    @classmethod
    def validate_date(cls, value):
        if value and value > date.today():
            raise ValueError("Expense date cannot be in the future")
        return value


class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        from_attributes = True