from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional

# SQLAlchemy Model
class SubscriptionDB(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String(255), nullable=False)
    event_type = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)

# Pydantic Model
class Subscription(BaseModel):
    target_url: HttpUrl
    event_type: str
    email: Optional[EmailStr] = None
    is_active: bool = True
