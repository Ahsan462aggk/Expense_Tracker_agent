# app/schemas/expense.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: str
    date: datetime  # Made required to align with SQLModel

class ExpenseCreate(ExpenseBase):
    user_id: int  # User ID is required for creation

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[datetime] = None  # Optional for partial updates

class ExpenseInDB(ExpenseBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
