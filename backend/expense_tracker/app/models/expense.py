from sqlmodel import Field, SQLModel,Relationship
from datetime import datetime
from typing import Optional

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment for ID
    amount: float
    description: str
    category: str
    date: datetime = Field(default_factory=datetime.utcnow)   # Automatically set the current UTC time if not provided
    user_id: int = Field(default=None, foreign_key="user.id") # Foreign key to User
    user: Optional["User"] = Relationship(back_populates="expenses") # Relationship to user