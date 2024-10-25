from database.laptopservice import *
from fastapi import UploadFile, File, APIRouter, HTTPException


# Создаем компонент
laptop_router = APIRouter(prefix='/laptops', tags=['Управление с Ноутбуками'])


# Добавить новый ноутбук
@laptop_router.post('/add-laptop')
async def add_laptop(
        model: str,
        monitor: str,
        brand: str,
        processor: str,
        ram: int,
        storage: str,
        gpu: str,
        price: float,
        stock_quantity: int,
        description: str,
        image: UploadFile = File(...)  # Принимаем изображение как UploadFile
):
    # Сохраняем изображение на сервере
    image_path = os.path.join(UPLOAD_DIR, image.filename)  # Формируем путь для сохранения изображения
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)  # Копируем содержимое файла в новый файл

    # Добавляем ноутбук с путем к изображению
    laptop = add_laptop_db(model, monitor, brand, processor, ram, storage, gpu, price, stock_quantity, description,
                           image_path)

    if laptop:
        return {"message": "Ноутбук успешно добавлен!", "laptop_id": laptop.laptop_id}
    else:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении ноутбука")


# Получить всех ноутбуков
@laptop_router.get('/all-laptops')
async def get_all_laptops():
    return get_all_laptops_db()


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