from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models import User, Laptop, Cart, CartItem
from database import get_db
from datetime import datetime

from sms.bot import send_order_notification
import random
import logging
logging.basicConfig(
    filename="monitoring&logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Показать товары в корзине пользователя
def get_all_in_cart_db(user_id: int):
    db = next(get_db())
    # Получаем корзину пользователя
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        logging.info("Корзина не найдена")
        return "Корзина не найдена."
    if not cart.items:
        logging.info("Корзина пуста")
        return "Корзина пуста."

    # Формируем список товаров, используя поле model вместо name
    return {
        "cart_id": cart.cart_id,
        "user_id": cart.user_id,
        "created_at": cart.created_at,
        "items": [
            {
                "item_id": item.item_id,
                "laptop_id": item.laptop.laptop_id,
                "laptop_model": item.laptop.model,  # Используем поле model
                "quantity": item.quantity,
            } for item in cart.items
        ]
    }


# Добавить товар в корзину
def add_to_cart_db(user_id: int, laptop_id: int, quantity: int = 1):
    db = next(get_db())

    # Проверяем наличие корзины у пользователя
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id, created_at=datetime.utcnow())
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Проверяем, есть ли товар в корзине
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.laptop_id == laptop_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.cart_id, laptop_id=laptop_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return {"message": "Товар добавлен в корзину", "cart_item": cart_item}


# Удалить товар из корзины
def remove_from_cart_db(user_id: int, laptop_id: int):
    db = next(get_db())

    # Проверяем, есть ли корзина у пользователя
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        logging.info("Корзина не найдена")
        return "Корзина не найдена."

    # Удаляем элемент из корзины
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.laptop_id == laptop_id
    ).first()

    if not cart_item:
        logging.info("Товар не найден в корзине.")
        return "Товар не найден в корзине."

    db.delete(cart_item)
    db.commit()

    return {"message": "Товар удален из корзины"}


# Покупка товара
def purchase_cart_items(user_id: int):
    db: Session = next(get_db())

    # Получаем корзину и пользователя
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    user = db.query(User).filter(User.user_id == user_id).first()

    if not cart or not cart.items:
        logging.info("Корзина пуста или не найдена.")
        return "Корзина пуста или не найдена."
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Рассчитываем общую стоимость товаров в корзине
    total_price = 0
    for item in cart.items:
        laptop = db.query(Laptop).filter(Laptop.laptop_id == item.laptop_id).first()

        if laptop.stock_quantity < item.quantity:  # Проверка наличия товара на складе
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара: {laptop.model}. Доступно только {laptop.stock_quantity}."
            )

        # Увеличиваем общую стоимость
        total_price += laptop.price * item.quantity

    # Проверяем, достаточно ли средств на балансе
    if user.balance < total_price:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно средств. Ваш баланс: {user.balance}, а требуется: {total_price}."
        )

    # Обновляем баланс и количество товаров
    user.balance -= total_price
    for item in cart.items:
        laptop = db.query(Laptop).filter(Laptop.laptop_id == item.laptop_id).first()
        laptop.stock_quantity -= item.quantity  # Уменьшаем количество на складе

    # Очищаем корзину после покупки
    for item in cart.items:
        db.delete(item)

    try:
        order_id = random.randint(100000, 999999)
        send_order_notification(order_id)
        db.commit()
    except Exception as e:
        db.rollback()  # Откатываем изменения при ошибке
        raise HTTPException(status_code=500, detail="Произошла ошибка во время покупки: " + str(e))
    return "Покупка завершена, средства списаны, корзина очищена."

# Добавить смс о доставке ноутбука