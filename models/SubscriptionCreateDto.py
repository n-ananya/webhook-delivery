from pydantic import BaseModel
from typing import Optional, Dict
from dataclasses import field

#PyDantic Model
class SubscriptionCreateDto(BaseModel):
    name: str
    tier: str
    email: str
    description: Optional[str] = field(default=None)
    metadata: Optional[Dict[str,str]] = {}

    class Config:
        orm_mode = True
