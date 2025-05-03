from pydantic import BaseModel


class WebhookDto(BaseModel):
    id: str
    target_url: str

    class Config:
        orm_mode = True