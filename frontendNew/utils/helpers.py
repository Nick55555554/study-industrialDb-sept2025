import uuid
from datetime import datetime

def generate_id() -> str:
    """Генерация UUID"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Получение текущей даты и времени"""
    return datetime.now().isoformat()