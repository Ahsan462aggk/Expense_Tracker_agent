# app/schemas/token_with_user.py

from pydantic import BaseModel
from typing import Optional
from app.schemas.token import Token
from app.schemas.user import UserRead

class TokenWithUser(BaseModel):
    access_token: str
    token_type: str
    user: UserRead
