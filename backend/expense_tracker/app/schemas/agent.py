# app/schemas/agent.py

from pydantic import BaseModel
from typing import Optional

class AgentQueryRequest(BaseModel):
    messages: str

class AgentQueryResponse(BaseModel):
    response: str
