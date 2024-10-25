from database.models import User, Laptop
from database import get_db
from laptops import LaptopValidator

from fastapi import UploadFile
import shutil
import os

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Добавить новый ноутбук
def add_laptop_db(model, monitor, brand, processor, ram, storage, gpu, price, stock_quantity, description, image_url):
    db = next(get_db())

    new_laptop = Laptop(
        model=model,
        monitor=monitor,
        brand=brand,
        processor=processor,
        ram=ram,
        storage=storage,
        gpu=gpu,
        price=price,
        stock_quantity=stock_quantity,
        description=description,
        image_url=image_url
    )

    db.add(new_laptop)
    db.commit()
    db.refresh(new_laptop)
    return new_laptop  # Возвращаем объект ноутбука для дальнейшего использования


# Получить всех ноутбуков
def get_all_laptops_db():
    db = next(get_db())

    get_all_laptops = db.query(Laptop).all()

    return get_all_laptops


# Удалить ноутбук
def delete_laptop_db(laptop_id):
    db = next(get_db())

    delete_laptop = db.query(Laptop).filter_by(laptop_id=laptop_id).first()

    if delete_laptop:
        db.delete(delete_laptop)
        db.commit()
        return 'Ноутбук удален из продажи успешно!'
    else:
        return 'Ноутбук не найден в продаже!'

# Редактировать ноутбук
def edit_laptop_db(laptop_id, edit_info, new_info):
    db = next(get_db())

    exact_laptop = db.query(Laptop).filter_by(laptop_id=laptop_id).first()

    if exact_laptop:
        if edit_info == 'model':
            exact_laptop.model = new_info
        elif edit_info =='monitor':
            exact_laptop.monitor = new_info
        elif edit_info == 'brand':
            exact_laptop.brand = new_info
        elif edit_info == 'processor':
            exact_laptop.processor = new_info
        elif edit_info == 'ram':
            exact_laptop.ram = new_info
        elif edit_info == 'storage':
            exact_laptop.storage = new_info
        elif edit_info == 'gpu':
            exact_laptop.gpu = new_info
        elif edit_info == 'price':
            exact_laptop.price = new_info
        elif edit_info =='stock_quantity':
            exact_laptop.stock_quantity = new_info
        elif edit_info == 'description':
            exact_laptop.description = new_info

        db.commit()
        return 'Данные ноутбука успешно изменены!'
    else:
        return 'Ноутбук не найден!'


