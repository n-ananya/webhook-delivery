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

@app.post("/subscription")
def create_subscription(subscriptiondto: SubscriptionDto, db: Session = Depends(get_db)):
    try:
        print("Request: " + str(subscriptiondto))
        db_subscription = Subscription(id=str(uuid.uuid4()),name = subscriptiondto.name)
        subscriptions[db_subscription.id] = db_subscription
        print(subscriptions)
        return {"subscription_id": db_subscription.id, "name": db_subscription.name}
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/subscription/{id}")
def get_subscription(id: str):
    try:
        return subscriptions[id]
    except KeyError as e:
        return HTTPException(status_code=404, detail="User Not Found")

@app.put("/subscription")
def update_subscription(subscriptiondto: SubscriptionDto):
    subscription = subscriptions[subscriptiondto.id]
    subscription.name = subscriptiondto.name
    subscriptions[subscriptiondto.id] = subscription
    return subscription

@app.delete("/subscription/{id}")
def delete_sub(id: str):
    subscriptions.pop(id)
    return "Subscription Deleted"

