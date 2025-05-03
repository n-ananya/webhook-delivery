from sqlalchemy import JSON, Column, CHAR, String, Boolean, DateTime
from database.database import Base

# Define the Subscription model
class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(CHAR(36), primary_key=True, index=True)
    name = Column(String(200))
    tier = Column(String(50))
    email = Column(String(100), index=True)
    description = Column(String(1024))
    sub_metadata = Column('metadata', JSON)


    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    expires_at = Column(DateTime)
