import json
import os
from typing import List, Dict, Any

class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename
    
    def load_data(self) -> List[Dict[str, Any]]:
        """Загрузка данных из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_data(self, data: List[Dict[str, Any]]):
        """Сохранение данных в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)