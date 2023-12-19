from pydantic import BaseModel
from typing import Optional

# Расширенная модель для услуги
class Service(BaseModel):
    name: str = 'Удаление зуба'
    price: str = '1000р'
    doctor: str = 'Иванов И.И.'
    room_number: str = '304'
    description: str = 'С обезболивающим'