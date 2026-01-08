from pydantic import BaseModel,Field
from typing import Optional
from datetime import date



class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0, description="Expense amount must be greater than 0")
    category: str = Field(..., min_length=1)
    description: Optional[str] = None
    expense_date: Optional[date] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    expense_date: Optional[date] = None


class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        from_attributes = True