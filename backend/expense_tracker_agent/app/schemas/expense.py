from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime

class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: str
    date:Optional[datetime]

class ExpenseCreate(ExpenseBase):
    user_id: int  # User ID is required for creation

class ExpenseUpdate(ExpenseBase):
    user_id: Optional[int] = None  # Optional for updates

class ExpenseInDB(ExpenseBase):
    id: int
    date: datetime
    user_id: Optional[int]=None
    model_config = ConfigDict(from_attributes=True)
