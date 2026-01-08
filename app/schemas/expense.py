from pydantic import BaseModel
from typing import Optional


class ExpenseBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
