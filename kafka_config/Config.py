import requests
from kafka import KafkaProducer, KafkaConsumer

from WebhookDto import WebhookDto
from entities.InMemorySubscription import subscriptions
from models.SubscriptionCreateDto import SubscriptionCreateDto

producer = KafkaProducer(bootstrap_servers='localhost:9092')


def consume_messages():
    consumer = KafkaConsumer(
        'webhook_payload',
    bootstrap_servers='localhost:9092',
        group_id='webhook_payload_reader',
        auto_offset_reset='earliest'
    )
    for message in consumer:
        try:
            sub_obj_str = message.value.decode('utf-8')
            print(f"Received message: {sub_obj_str}")
            webhook_dto = WebhookDto.model_validate_json(sub_obj_str)
            print(f"target_url: {webhook_dto.target_url}")
            sub_id = webhook_dto.id
            sub_dto = subscriptions[sub_id]
            post_to_webhook(sub_dto, webhook_dto.target_url)
        except Exception as e:
            print('Exception Occurred while consuming message: ' + str(e))

def post_to_webhook(sub: SubscriptionCreateDto, target_url: str):
    try:
        requestBody = {"id": sub.id, "name": sub.name}
        requests.post(target_url, json=requestBody)
        print('WebHook request sent for id:' + str(sub.id))
    except Exception as e:
        print('Exception Occurred while sending webhook request: ' + str(e))

