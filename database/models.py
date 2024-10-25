from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# Модель пользователя
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)  # Уникальный идентификатор пользователя
    username = Column(String)  # Имя пользователя
    surname = Column(String)  # Фамилия пользователя
    phone_number = Column(String, unique=True)  # Телефонный номер, уникальный для каждого пользователя
    address = Column(String)  # Адрес пользователя
    balance = Column(Float, default=0)  # Баланс пользователя
    password = Column(String)  # Пароль пользователя

    # Связи с другими моделями
    cards = relationship("Card", back_populates="user")  # Связь с картами
    laptops = relationship("Laptop", back_populates="user")  # Связь с ноутбуками
    carts = relationship("Cart", back_populates="user")  # Связь с корзинами


# Модель карты
class Card(Base):
    __tablename__ = 'cards'

    card_id = Column(Integer, primary_key=True)  # Уникальный идентификатор карты
    user_id = Column(Integer, ForeignKey('users.user_id'))  # Внешний ключ на пользователя
    card_number = Column(String, unique=True)  # Номер карты, уникальный для каждой карты
    card_type = Column(String)  # Тип карты (например, Visa, MasterCard)
    card_data = Column(String)  # Срок действия карты
    card_cvv = Column(String)  # CVV код

    user = relationship("User", back_populates="cards")  # Связь с пользователем


# Модель ноутбука
class Laptop(Base):
    __tablename__ = 'laptops'

    laptop_id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)  # Уникальный идентификатор ноутбука
    model = Column(String)  # Модель ноутбука
    monitor = Column(String)  # Размер или тип монитора
    brand = Column(String)  # Производитель ноутбука
    processor = Column(String)  # Процессор
    ram = Column(Integer)  # Объем оперативной памяти
    storage = Column(String)  # Объем и тип накопителя
    gpu = Column(String)  # Графический процессор
    price = Column(Float)  # Цена ноутбука
    stock_quantity = Column(Integer)  # Количество ноутбуков на складе
    description = Column(Text)  # Описание ноутбука
    image_url = Column(String)  # Ссылка на изображение ноутбука

    user_id = Column(Integer, ForeignKey('users.user_id'))  # Внешний ключ на пользователя (владелец ноутбука)
    user = relationship("User", back_populates="laptops")  # Связь с пользователем


# Модель корзины
class Cart(Base):
    __tablename__ = 'carts'

    cart_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  # Уникальный идентификатор корзины
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Внешний ключ на пользователя
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания корзины

    user = relationship("User", back_populates="carts")  # Связь с пользователем
    items = relationship("CartItem", back_populates="cart")  # Связь с товарами в корзине


# Модель элемента корзины
class CartItem(Base):
    __tablename__ = 'cart_items'

    item_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  # Уникальный идентификатор элемента
    cart_id = Column(Integer, ForeignKey('carts.cart_id'), nullable=False)  # Внешний ключ на корзину
    laptop_id = Column(Integer, ForeignKey('laptops.laptop_id'), nullable=False)  # Внешний ключ на ноутбук
    quantity = Column(Integer, default=1)  # Количество данного ноутбука в корзине

    cart = relationship("Cart", back_populates="items")  # Связь с корзиной
    laptop = relationship("Laptop")  # Связь с ноутбуком

