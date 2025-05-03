from pydantic import BaseModel

#PyDantic Model
class SubscriptionDto(BaseModel):
    name: str

    class Config:
        orm_mode = True
