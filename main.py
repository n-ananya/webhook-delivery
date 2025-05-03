import asyncio
import logging
import threading
import uuid

from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy import text, MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from WebhookDto import WebhookDto
from database.database import Base, engine
from database.database import get_db
from entities.Subscription import Subscription
from kafka_config.Config import producer
from kafka_config.Consumer import consume_messages
from models.SubscriptionCreateDto import SubscriptionCreateDto

logging.basicConfig(
    level=logging.INFO,  # Use INFO or WARNING in production
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()




@app.post("/subscription")
def create_subscription(subscriptiondto: SubscriptionCreateDto, db: Session = Depends(get_db)):
    try:
        print("Request: " + str(subscriptiondto))
        sub = create_sub_entity_from_dto(subscriptiondto)
        db.add(sub)
        db.commit()
        print(sub)
        return SubscriptionCreateDto.from_orm(sub)
    except IntegrityError as e:
        print('Duplicate Data Found: ' + str(e))
        raise HTTPException(status_code=400, detail="Same Detail ALready Exists")
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/subscription/{id}")
def get_subscription(id: str, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == id).first()
    if sub is None:
        return HTTPException(status_code=404, detail="User Not Found")
    return SubscriptionCreateDto.from_orm(sub)

@app.put("/subscription")
def update_subscription(subscriptiondto: SubscriptionCreateDto, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == subscriptiondto.id)
    if sub is None:
        return HTTPException(status_code=404, detail="User Not Found")
    update_sub_entity_from_dto(subscriptiondto, sub)
    db.commit()
    return SubscriptionCreateDto.from_orm(sub)

@app.delete("/subscription/{id}")
def delete_sub(id: str, db: Session = Depends(get_db)):
    db.query(Subscription).filter(Subscription.id == id).delte()
    db.commit()
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

@app.on_event("startup")
def on_startup():
    ## validate existing database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    ## create tables
    print("Creating database tables if does not exists")
    Base.metadata.create_all(bind=engine)

    ## start kafka consumer here
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

def create_sub_entity_from_dto(sub_dto: SubscriptionCreateDto):
    now = func.now()
    return Subscription(
        id = str(uuid.uuid4()),
        name = sub_dto.name,
        tier = sub_dto.tier,
        email = sub_dto.email,
        description = sub_dto.description,
        sub_metadata = None,
        is_active = True,
        created_at = now,
        updated_at = None,
        expires_at = now + text("INTERVAL 1 MONTH")
    )

def update_sub_entity_from_dto(sub_dto: SubscriptionCreateDto, sub_existing: Subscription):
    sub_existing.name = sub_dto.name
    sub_existing.tier = sub_dto.tier
    sub_existing.email = sub_dto.email
    sub_existing.description = sub_dto.description
    sub_existing.sub_metadata = None
    sub_existing.updated_at = func.now()
    return sub_existing



