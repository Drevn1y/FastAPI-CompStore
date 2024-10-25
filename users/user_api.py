from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.userservice import *
from users import RegisterValidator, EditUserValidator

# Создаем компонент
user_router = APIRouter(prefix='/users', tags=['Управление с пользователями'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Запрос для регистрации
@user_router.post('/register')
async def register_user(data: RegisterValidator):
    result = register_user_db(**data.model_dump())

    if result:
        return {'message': result}
    else:
        return {'message': 'Такой пользователь уже зарегестрирован!'}


# Запрос для входа
@user_router.post('/login')
async def login_user(from_data: OAuth2PasswordRequestForm = Depends()):
    user = login_user_db(from_data.username, from_data.password)

    if not user:
        raise HTTPException(status_code=400, detail='Неверный номер или пароль')
    else:
        return user


# Запрос на получения всех юзеров
@user_router.get('/all-user')
async def get_all_users():
    return get_all_users_db()


# Запрос на получения определенного пользователя
@user_router.get('/user')
async def get_user(user_id: int):
    exact_user = get_exact_user_db(user_id)
    return exact_user


# Запрос на редактирование
@user_router.put('/edit')
async def edit_user_db(data: EditUserValidator):
    change_data = data.model_dump()
    result = edit_user_info_db(**change_data)
    return result


# Запрос на удаления пользователя
@user_router.delete('/delete-user')
async def delete_user(user_id):
    user = delete_user_db(user_id)
    return user


# Пополнение балланса
@user_router.put('/plus-balance')
async def plus_balance(user_id: int, card_number: str, amount: float):
    result = plus_balance_user_db(user_id, card_number, amount)
    return result


# Списание из балланса
@user_router.put('/pay-balance')
async def minus_balance(user_id, balance: float):
    result = minus_balance_user_db(user_id=user_id, balance=balance)

    return result


# Просмотр баланса пользователя
@user_router.get('/user-balance/{user_id}')
async def show_balance_user(user_id: int):
    balance = show_balance_user_db(user_id)
    if isinstance(balance, str):
        return {"message": balance}
    else:
        return {"balance": balance}
