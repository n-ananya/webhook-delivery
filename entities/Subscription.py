from sqlalchemy import Column, Integer, String
from database.database import Base

# Define the Subscription model
class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    # email = Column(String, index=True)
    # plan = Column(String)