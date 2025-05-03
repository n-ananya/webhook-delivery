from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal, engine, Base
from models.subscription import Subscription, SubscriptionDB

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/subscriptions/")
def create_subscription(subscription: Subscription, db: Session = Depends(get_db)):
    db_subscription = SubscriptionDB(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return {"subscription_id": db_subscription.id, "details": subscription}
