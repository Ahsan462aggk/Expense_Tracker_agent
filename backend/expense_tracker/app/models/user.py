from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # New field
    expenses: List["Expense"] = Relationship(back_populates="user")  # Relationship to expenses

    def verify_password(self, password: str) -> bool:
        from passlib.hash import bcrypt
        return bcrypt.verify(password, self.hashed_password)
