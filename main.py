import logging
import threading

from fastapi import FastAPI
from sqlalchemy import MetaData

from api.SubscriptionAPI import sub_router
from api.WebHookAPI import webhook_router
from database.database import Base, engine
from kafka_config.Consumer import consume_messages

logging.basicConfig(
    level=logging.INFO,  # Use INFO or WARNING in production
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

#include router from subscription API and webhook API 
app.include_router(sub_router)
app.include_router(webhook_router)

@app.on_event("startup")
def on_startup():
    ## validate existing database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    ## create tables
    print("Creating database tables if does not exists")
    Base.metadata.create_all(bind=engine)

    ## start kafka consumer Thread here
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()



