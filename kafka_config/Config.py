from kafka import KafkaProducer, KafkaConsumer
import threading

producer = KafkaProducer(bootstrap_servers='localhost:9092')


def consume_messages():
    consumer = KafkaConsumer(
        'webhook_payload',
    bootstrap_servers='localhost:9092',
        group_id='webhook_payload_reader',
        auto_offset_reset='earliest'
    )
    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")

consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.start()

