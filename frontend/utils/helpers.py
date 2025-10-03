import uuid
from datetime import datetime

def generate_id() -> str:
    """Генерация UUID"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Получение текущей даты и времени в ISO формате"""
    return datetime.now().isoformat()

def format_date_for_display(date_string: str) -> str:
    """Форматирование даты для отображения"""
    try:
        if "T" in date_string:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        else:
            dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return date_string