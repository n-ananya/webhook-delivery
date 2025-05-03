import asyncio
from kafka_config.Config import producer
import logging

logger = logging.getLogger(__name__)

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