# Webhook Delivery Service

Webhook Delivery Service is a lightweight, event-driven backend system for managing subscriptions, ingesting payloads, delivering data asynchronously and retrying failed deliveries.



# Set Up Instructions

setup python virtual environment
python -m venv venv

activate venv script

.\bin\Scripts\Windows\activate.bat

install python module using pip

pip install -r requirements.txt


Run the app using:
uvicorn main:app --reload


# CRUD APIs


CREATE SUBSCRIPTION API

curl --location 'http://127.0.0.1:8000/ingestion' \
--header 'Content-Type: application/json' \
--data '{
  "id": "363294be-37e5-482f-b7fd-5a1be84c2713",
  "target_url": "https://webhook.site8932893892239/bd60ff53-14c3-4246-b363-0d7e4cbbbb28"
}'

READ SUBSCRIPTION API
curl --location 'http://127.0.0.1:8000/subscription/363294be-37e5-482f-b7fd-5a1be84c2713' \
--header 'Content-Type: application/json'

UPDATE SUBSCRIPTION API
curl --location --request PUT 'http://127.0.0.1:8000/subscription' \
--header 'Content-Type: application/json' \
--data '{
    "id": "f24feb54-b101-4431-a46c-41e4e15fc9e1",
  "name": "anshu"
}'

DELETE SUBSCRIPTION API
curl --location --request DELETE 'http://127.0.0.1:8000/subscription/12096dc0-27b9-47b1-989a-22b105dfbe5f' \
--header 'Content-Type: application/json'


#Webhook ingestion API

curl --location 'http://127.0.0.1:8000/ingestion' \
--header 'Content-Type: application/json' \
--data '{
  "id": "363294be-37e5-482f-b7fd-5a1be84c2713",
  "target_url": "https://webhook.site8932893892239/bd60ff53-14c3-4246-b363-0d7e4cbbbb28"
}'



 # Technologies Used 

 **Framework used**

 FASTAPI
 SQLAlchmey - ORM


 **Database used :** MySQL

 **Programming Language:** Python

 **Queue :** Kafka Messaging System


# Architecture

1. CRUD API interacts with db layer to read/save/update/delete subscription data
2. webhook ingestion api asynchronously adds webhook payload to kafka queue on topic "webhook_payload"
3. kafka message is consumed from webhook_payload and then related subscription is deliver to webhook url / target url
4. in case webhook delivery fails the subscription payload is then added to retry_sub topic on kafka
5. another consumer listens on retry_sub topic on kafka and attempt maximum 5 tries for sending webhook API
