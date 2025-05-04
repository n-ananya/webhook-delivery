from dataclasses import dataclass
from typing import Dict

from sqlalchemy import JSON, Column, CHAR, String, Boolean, DateTime, UniqueConstraint
from database.database import Base

# Define the Subscription model
class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(CHAR(36), primary_key=True, index=True)
    name = Column(String(200))
    tier = Column(String(50))
    email = Column(String(100), index=True, unique=True)
    description = Column(String(1024))
    sub_metadata = Column('metadata', JSON)


    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    expires_at = Column(DateTime)

    def to_dict(self) -> Dict[str,str]:
        return {
            'id': self.id,
            'name': self.name,
            'tier': self.tier,
            'email': self.email,
            'description': self.description,
            'metadata': self.sub_metadata,  # `sub_metadata` is a JSON column
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
