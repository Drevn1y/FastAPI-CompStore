from database.cartservice import *
from fastapi import APIRouter, HTTPException

# Создаем компонент
cart_router = APIRouter(prefix='/cart', tags=['Управление Корзиной'])

@cart_router.get('/get-all-in-cart/{user_id}')
async def get_all_in_cart(user_id: int):
    items = get_all_in_cart_db(user_id)
    if isinstance(items, str):  # Проверяем, если возвращена строка с сообщением
        raise HTTPException(status_code=404, detail=items)
    return items

@cart_router.post('/add-to-cart/')
async def add_to_cart(user_id: int, laptop_id: int, quantity: int = 1):
    result = add_to_cart_db(user_id, laptop_id, quantity)
    return result


@cart_router.delete('/remove-from-cart/')
async def remove_from_cart(user_id: int, laptop_id: int):
    result = remove_from_cart_db(user_id, laptop_id)
    if isinstance(result, str):  # Проверяем, если возвращена строка с сообщением
        raise HTTPException(status_code=404, detail=result)
    return result


@cart_router.post('/purchase/{user_id}')
async def purchase_items(user_id: int):
    try:
        # Вызываем функцию покупки товаров
        result = purchase_cart_items(user_id)
        return {"message": result}
    except HTTPException as e:
        # Если произошла ошибка (например, недостаток средств или товара)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Ловим любые другие ошибки
        raise HTTPException(status_code=500, detail="Произошла ошибка во время покупки")