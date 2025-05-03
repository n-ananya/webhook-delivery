import requests
from sqlalchemy.orm import Session

from WebhookDto import WebhookDto
from database.database import get_db
from entities.Subscription import Subscription
from kafka_config.Config import consumer


def consume_messages():
    for message in consumer:
        try:
            sub_obj_str = message.value.decode('utf-8')
            print(f"Received message: {sub_obj_str}")
            webhook_dto = WebhookDto.model_validate_json(sub_obj_str)
            print(f"target_url: {webhook_dto.target_url}")
            db: Session = next(get_db())
            sub: Subscription = db.query(Subscription).filter(Subscription.id==webhook_dto.id).one()
            post_to_webhook(sub, webhook_dto.target_url)
        except Exception as e:
            print('Exception Occurred while consuming message: ' + str(e))

def post_to_webhook(sub: Subscription, target_url: str):
    try:
        requests.post(target_url, json=sub.to_json())
        print('WebHook request sent for id:' + str(sub.id))
    except Exception as e:
        print('Exception Occurred while sending webhook request: ' + str(e))

