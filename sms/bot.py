# send_telegram.py
import telebot

# Задайте токен и чат ID напрямую
TELEGRAM_TOKEN = 'Token'  # Токен вашего бота
CHAT_ID = 'id'  # ID чата или пользователя, которому нужно отправить сообщение

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_order_notification(order_id: int):
    """
    Отправляет уведомление о принятии заказа через Telegram.
    :param order_id: ID заказа.
    """
    message = f"Ваш заказ #{order_id} принят и обрабатывается!"
    bot.send_message(CHAT_ID, message)
    print("Уведомление отправлено в Telegram.")

# Пример вызова
if __name__ == "__main__":
    example_order_id = 12345
    send_order_notification(example_order_id)
