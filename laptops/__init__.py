from pydantic import BaseModel


class LaptopValidator(BaseModel):
    laptop_id: int
    edit_info: str
    new_info: str
