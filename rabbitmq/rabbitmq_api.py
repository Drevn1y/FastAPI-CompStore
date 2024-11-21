from fastapi import APIRouter
from rabbitmq.rabbitmq_service import send_message, get_all_messages, delete_all_messages

from rabbitmq import MessageRequest

rabbit_router = APIRouter(prefix='/rabbitmq', tags=["Управление RabbitMQ"])

@rabbit_router.post("/send-message")
async def send_message_api(request: MessageRequest):
    """API для отправки сообщения в RabbitMQ."""
    await send_message(request.message)  # Отправляем сообщение в RabbitMQ
    return {"status": "Message sent"}

@rabbit_router.get("/get-all-messages")
async def get_all_messages_api():
    """API для получения всех сообщений из RabbitMQ."""
    messages = await get_all_messages()
    return {"messages": messages}

@rabbit_router.delete("/delete-all-messages")
async def delete_all_messages_api():
    """API для удаления всех сообщений из RabbitMQ."""
    await delete_all_messages()
    return {"status": "All messages deleted"}
