from sqlalchemy import Column, Integer, String, Float, Date
from datetime import date
from .database import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    expense_date = Column(Date, default=date.today)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    expenses = relationship("Expense", back_populates="user")