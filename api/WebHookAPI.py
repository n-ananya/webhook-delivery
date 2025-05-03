from fastapi import Response, status, APIRouter

from WebhookDto import WebhookDto
from kafka_config.Producer import send_async

webhook_router = APIRouter()

@webhook_router.post("/ingestion")
def ingest_webhook(web_hook_dto: WebhookDto):
    # produce web_hook_dto json to kafka_config
    send_async(web_hook_dto.model_dump_json())
    return Response(status_code = status.HTTP_202_ACCEPTED)