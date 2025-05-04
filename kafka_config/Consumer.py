import json

import requests
from sqlalchemy.orm import Session

from WebhookDto import WebhookDto
from database.database import get_db
from entities.Subscription import Subscription
from kafka_config.Config import consumer, retry_consumer
import asyncio

from kafka_config.Producer import send_async


async def consume_async_await():
    loop = asyncio.get_event_loop()
    tasks = [

     loop.run_in_executor(None, consume_messages_webhook),
     loop.run_in_executor(None, consume_messages_retry),
    ]
    results = await asyncio.gather(*tasks)

def consume_messages_webhook():
    for message in consumer:
        sub_obj_str = message.value.decode('utf-8')
        print(f"Received message: {sub_obj_str}")
        webhook_dto = WebhookDto.model_validate_json(sub_obj_str)
        sub_dict : Subscription = None
        try:
            print(f"target_url: {webhook_dto.target_url}")
            db: Session = next(get_db())
            sub: Subscription = db.query(Subscription).filter(Subscription.id==webhook_dto.id).one()
            sub_dict = sub.to_dict()
            post_to_webhook(sub_dict, webhook_dto.target_url)
        except Exception as e:
            print('Exception Occurred while consuming message: ' + str(e))
            if sub_dict is not None:
                send_to_retry_topic(sub_dict, webhook_dto.target_url, 1)

def consume_messages_retry():
    for message in retry_consumer:
        try:
            retry_dto_str = message.value.decode('utf-8')
            print(f"Received message: {retry_dto_str}")
            retry_dto = json.loads(retry_dto_str)
            retry_count = retry_dto["ret"]
            if retry_count > 5:
                print("Maximum retry reached returning")
            else:
                sub_json = retry_dto["sub"]
                sub_dict = json.loads(sub_json)
                target_url = retry_dto["target_url"]
                try:
                    post_to_webhook(sub_dict, target_url)
                except Exception as e_inner:
                    print("Exception Occurred while retrying post webhook: " + str(e_inner))
        except Exception as e:
            print('Exception Occurred while retrying message: ' + str(e))

def send_to_retry_topic(sub: dict, target_url: str, retry_count: int):
    try:
        sub_retry_dto = generate_retry_payload(retry_count, json.dumps(sub), target_url)
        send_async(json.dumps(sub_retry_dto), 'retry_sub')
    except Exception as e:
        print('Exception occurred while trying to send to retry_topic: '+ str(e))

def post_to_webhook(sub: dict, target_url: str):
    requests.post(target_url, json=json.dumps(sub))
    print('WebHook request sent for id:' + str(sub.id))

def generate_retry_payload(retry_count: int, sub, target_url: str):
    return {
        "ret": retry_count,
        "sub": sub,
        "target_url": target_url
    }

