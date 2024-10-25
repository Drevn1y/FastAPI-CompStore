from fastapi import APIRouter, Depends, HTTPException
from database.laptopservice import *


# Создаем компонент
laptop_router = APIRouter(prefix='/laptops', tags=['Управление с Ноутбуками'])


# Получить всех ноутбуков
@laptop_router.get('/all-laptops')
async def get_all_laptops():
    return get_all_laptops_db()


# Добавить новый ноутбук
@laptop_router.post('/add-laptop')
async def add_laptop(model, monitor, brand, processor, ram, storage, gpu, price, stock_quantity, description, image_url):
    laptop = add_laptop_db(model, monitor, brand, processor, ram, storage, gpu, price, stock_quantity, description, image_url)
    if laptop:
        return 'Успешно добавлено!'
    else:
        return 'Что-то пошло не так'


# Удалить ноутбук
@laptop_router.delete('/delete-laptop/{laptop_id}')
async def delete_laptop(laptop_id):
    return delete_laptop_db(laptop_id)


# Редактировать ноутбук
@laptop_router.put('/edit-laptop/{laptop_id}')
async def edit_laptop(data: LaptopValidator):
    change_data = data.model_dump()
    result = edit_laptop_db(**change_data)
    return result