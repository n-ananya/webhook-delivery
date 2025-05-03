import logging
import threading

from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy import text, MetaData


from WebhookDto import WebhookDto
from database.database import Base, engine
from kafka_config.Consumer import consume_messages
from kafka_config.Producer import send_async

logging.basicConfig(
    level=logging.INFO,  # Use INFO or WARNING in production
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/ingestion")
def ingest_webhook(web_hook_dto: WebhookDto):
    # produce web_hook_dto json to kafka_config
    send_async(web_hook_dto.model_dump_json())
    return Response(status_code = status.HTTP_202_ACCEPTED)




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



