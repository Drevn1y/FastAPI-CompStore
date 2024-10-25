from pydantic import BaseModel

# Валидатор для регистрации
class RegisterValidator(BaseModel):
    username: str
    surname: str
    phone_number: str
    password: str


# Валидатор для редактирования
class EditUserValidator(BaseModel):
    user_id: int
    edit_info: str
    new_info: str
