import aio_pika
import asyncio
from typing import List

RABBITMQ_URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "my_queue"


async def connect_to_rabbitmq():
    """Подключение к RabbitMQ и создание канала."""
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return connection


async def send_message(message: str):
    """Отправка сообщения в очередь RabbitMQ."""
    connection = await connect_to_rabbitmq()
    async with connection:
        channel = await connection.channel()  # Создаем канал
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)  # Декларируем очередь
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),  # Публикуем сообщение
            routing_key=queue.name,
        )
        print(f"Message sent: {message}")


async def get_all_messages() -> List[str]:
    """Получение всех сообщений из RabbitMQ."""
    connection = await connect_to_rabbitmq()
    messages = []

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        while True:
            try:
                # Получаем одно сообщение из очереди
                message = await queue.get(no_ack=False)
                if message is None:
                    # Если сообщение отсутствует, завершаем цикл
                    break

                # Добавляем текст сообщения в список
                messages.append(message.body.decode())
                await message.ack()  # Подтверждаем обработку сообщения

            except aio_pika.exceptions.QueueEmpty:
                # Если очередь пуста, завершаем цикл
                break

        return messages


async def delete_all_messages():
    """Удаление всех сообщений из RabbitMQ."""
    connection = await connect_to_rabbitmq()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await queue.purge()  # Очищаем очередь
        print("All messages have been deleted.")
