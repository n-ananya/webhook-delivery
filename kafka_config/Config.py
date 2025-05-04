from kafka import KafkaProducer, KafkaConsumer



producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer(
    'webhook_payload',
    bootstrap_servers='localhost:9092',
    group_id='webhook_payload_reader',
    auto_offset_reset='earliest'
)

retry_consumer = KafkaConsumer(
    'retry_sub',
    bootstrap_servers='localhost:9092',
    group_id='webhook_payload_reader',
    auto_offset_reset='earliest'
)