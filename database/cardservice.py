from database.models import User, Card

from database import get_db
from database.security import create_access_token


# Функция для добавления карты пользователю
def add_card_to_user_db(user_id: int, card_number: str, card_type: str, card_data: str, card_cvv: str):
    db = next(get_db())

    # Проверка, существует ли пользователь
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        return {'message': 'Пользователь не найден'}

    # Проверка, существует ли уже карта с таким номером
    existing_card = db.query(Card).filter_by(card_number=card_number).first()
    if existing_card:
        return {'message': 'Карта с таким номером уже существует'}

    # Создание новой карты
    new_card = Card(
        user_id=user_id,
        card_number=card_number,
        card_type=card_type,
        card_data=card_data,
        card_cvv=card_cvv
    )

    # Добавление карты в базу данных
    db.add(new_card)
    db.commit()

    return {'message': f'Карта c айди {card_number} успешно добавлена пользователю {user.username}'}


# Функция для удаления карты пользователя
def delete_card_db(user_id, card_number):
    db = next(get_db())

    # Поиск пользователя
    user = db.query(User).filter(User.user_id == user_id).first()

    # Поиск карты
    card = db.query(Card).filter_by(card_number=card_number, user_id=user_id).first()

    # Проверка, существует ли пользователь и карта
    if user and card:
        db.delete(card)
        db.commit()
        return f'Карта {card_number} удалена успешно!'
    else:
        return 'Пользователь или карта не найдена'



# Функция для просмотра карт пользователя
def get_card_db(user_id):
    db = next(get_db())

    # Поиск карт, связанных с пользователем
    cards = db.query(Card).filter_by(user_id=user_id).all()

    if not cards:
        return {'message': 'Карты не найдены'}

    # Возвращение информации о всех картах
    return [
        {
            'card_number': card.card_number,
            'card_type': card.card_type,
            'card_data': card.card_data,
            'card_cvv': card.card_cvv
        }
        for card in cards
    ]
