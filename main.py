from fastapi import FastAPI, Depends, HTTPException
from models.SubscriptionDto import SubscriptionDto
from entities.Subscription import Subscription
from sqlalchemy.orm import Session
from database.database import SessionLocal
import uuid
import logging


logging.basicConfig(
    level=logging.DEBUG,  # Use INFO or WARNING in production
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Dependency to get the database session
def get_db():
    print("Inside get_db()")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

subscriptions = {}

@app.post("/subscriptions")
def create_subscription(subscriptiondto: SubscriptionDto, db: Session = Depends(get_db)):
    try:
        print("Request: " + str(subscriptiondto))
        db_subscription = Subscription(id=uuid.uuid4(),name = subscriptiondto.name)
        subscriptions[db_subscription.id] = db_subscription
        return {"subscription_id": db_subscription.id, "name": db_subscription.name}
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")