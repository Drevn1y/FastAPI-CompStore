from database.models import User, Card

from database import get_db
from database.security import create_access_token


# Получить всех пользователей
def get_all_users_db():
    db = next(get_db())

    get_all_users = db.query(User).all()

    return get_all_users


# Получить определенного пользователя
def get_exact_user_db(user_id):
    db = next(get_db())

    checker = db.query(User).filter_by(user_id=user_id).first()

    if checker:
        found_user = {
            'user_id': checker.user_id,
            'username': checker.username,
            'surname': checker.surname,
            'phone_number': checker.phone_number,
            'address': checker.address,
            'balance': checker.balance,
        }
        return f'Пользователь найден {found_user}'
    else:
        return 'Пользователь не обнаружен'


# Регистрация пользователя
def register_user_db(username, surname, phone_number, password):
    db = next(get_db())

    checker = db.query(User).filter_by(phone_number=phone_number).first()

    if checker:
        return 'Такой номер телефона уже есть в базу'
    else:
        new_user = User(username=username, surname=surname, phone_number=phone_number, password=password)
        db.add(new_user)
        db.commit()
        return f'Успешно зарегистрированы {new_user.user_id}'


# Логин
def login_user_db(username, password):
    db = next(get_db())

    login = db.query(User).filter_by(username=username, password=password).first()

    if login:
        token_data = {"user_id": login.user_id}
        access_token_data = create_access_token(token_data)
        return {"access_token": access_token_data, "token_type": "Bearer", "status": "Success"}
    else:
        return 'Неверный номер телефона или пароль'


#  Удаления пользователя
def delete_user_db(user_id):
    db = next(get_db())
    user = db.query(User).filter_by(user_id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return f'Пользователь с ID {user_id} удален'
    else:
        return 'Пользователь не найден'


# Изменения данных пользователя
def edit_user_info_db(user_id, edit_info, new_info):
    db = next(get_db())

    exact_user = db.query(User).filter_by(user_id=user_id).first()  # 3

    if exact_user:
        if edit_info == 'username':
            exact_user.username = new_info
        elif edit_info == 'surname':
            exact_user.surname = new_info
        elif edit_info == 'phone_number':
            exact_user.phone_number = new_info
        elif edit_info == 'address':
            exact_user.address = new_info
        elif edit_info == 'password':
            exact_user.password == new_info

        db.commit()
        return 'Данные успешно изменены!'
    else:
        return 'Пользователь не найден(('


# Пополнить баланс
def plus_balance_user_db(user_id: int, card_number: str, amount: float):
    db = next(get_db())

    # Проверка на наличие пользователя
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        return {'message': 'Пользователь не найден'}

    # Проверка на наличие карты у пользователя
    card = db.query(Card).filter_by(card_number=card_number, user_id=user_id).first()
    if not card:
        return {'message': 'Карта не найдена или не принадлежит пользователю'}

    # Проверка суммы пополнения (должна быть больше 0)
    if amount <= 0:
        return {'message': 'Сумма пополнения должна быть больше 0'}

    # Пополнение баланса
    user.balance += amount
    db.commit()  # Сохраняем изменения в базе данных

    return {'message': f'Баланс пополнен на {amount}. Текущий баланс: {user.balance}'}


# Списание с баланса вывод денег
def minus_balance_user_db(user_id, balance: float):
    db = next(get_db())

    user = db.query(User).filter_by(user_id=user_id).first()

    if user:
        if user.balance >= balance:  # Проверяем, достаточно ли денег на балансе
            user.balance -= balance
            db.commit()
            return f"Вы вывели свои деньги. Ваш балланс на сайте: {user.balance} $"
        else:
            return f"В вашем баллансе недостаточно денег!"
    else:
        return f"Пользователь с id {user_id} не найден!"


# Просмотр баланса пользователя в базе данных
def show_balance_user_db(user_id):
    db = next(get_db())

    user = db.query(User).filter_by(user_id=user_id).first()

    if user:
        return f'{user.balance}$'
    else:
        return 'Пользователь не найден'



