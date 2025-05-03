from pydantic import BaseModel
from typing import Optional, Dict
from dataclasses import field

#PyDantic Model
class SubscriptionCreateDto(BaseModel):
    id: Optional[str] = field(default=None)
    name: str
    tier: str
    email: str
    description: Optional[str] = field(default=None)
    #metadata: Optional[Dict[str,str]] = field(default=None)

    class Config:
        orm_mode = True
        from_attributes=True
