from pydantic import BaseModel

class MessageRequest(BaseModel):
    """Ожидаемое сообщение от клиента"""
    message: str


