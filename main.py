from fastapi import FastAPI, Depends, HTTPException, Response, status

from WebhookDto import WebhookDto
from models.SubscriptionDto import SubscriptionDto
from entities.Subscription import Subscription
from sqlalchemy.orm import Session
from database.database import SessionLocal
import uuid
import logging
from kafka_config.Config import producer
from entities.InMemorySubscription import subscriptions
import asyncio


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

@app.post("/ingestion")
def ingest_webhook(web_hook_dto: WebhookDto):
    # produce web_hook_dto json to kafka_config
    send_async(web_hook_dto.model_dump_json())
    return Response(status_code = status.HTTP_202_ACCEPTED)


def send_async(payload: str):
    asyncio.run(async_send_message(payload))

async def async_send_message(payload: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, send_message, payload)

def send_message(msg: str):
    try:
        producer.send('webhook_payload', msg.encode('UTF-8'))
        producer.flush()
        logger.info("Kafka Message Produced: ", )
    except Exception as e:
        logger.info("Exception Occurred while producing: ", e)



