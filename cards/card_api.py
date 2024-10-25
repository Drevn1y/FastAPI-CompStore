from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.cardservice import *

# Создаем компонент
card_router = APIRouter(prefix='/cards', tags=['Управление с картами'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Асинхронная функция для обработки запроса на добавление карты
@card_router.post('/user/{user_id}/add_card')
async def add_card(user_id: int, card_number: str, card_type: str, card_data: str, card_cvv: str):
    response = add_card_to_user_db(user_id, card_number, card_type, card_data, card_cvv)
    return response


# Функция для просмотра карт пользователя
@card_router.post('/get_card')
async def get_card(user_id: int):
    cards = get_card_db(user_id=user_id)
    return cards


# Удалить карту
@card_router.post('/delete_card')
async def delete_card(user_id: int, card_number: str):
    card = delete_card_db(user_id=user_id, card_number=card_number)
    return card
