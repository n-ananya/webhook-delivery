from pydantic import BaseModel
from typing import Optional

#PyDantic Model
class SubscriptionDto(BaseModel):
    id: Optional[str] = None
    name: str

    class Config:
        orm_mode = True
