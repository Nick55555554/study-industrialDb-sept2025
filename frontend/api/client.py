import requests
import json
from typing import List, Dict, Any

class DDOSApiClient:
    def __init__(self, base_url: str = "http://localhost:3000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def check_database_status(self) -> Dict[str, Any]:
        """Проверка статуса БД"""
        try:
            response = self.session.get(f"{self.base_url}/database/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error checking database status: {e}")
            # Возвращаем статус по умолчанию при ошибке
            return {"success": False, "data": {"tablesExist": False}}

    def initialize_database(self) -> Dict[str, Any]:
        """Создание таблиц"""
        try:
            response = self.session.post(f"{self.base_url}/database/init")
            # Если таблицы уже существуют (409), это не ошибка для нас
            if response.status_code == 409:
                return {
                    "success": True,
                    "message": "Tables already exist",
                    "status": "already_exists"
                }
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Если это конфликт (таблицы уже существуют), обрабатываем как успех
            if "409" in str(e):
                return {
                    "success": True,
                    "message": "Tables already exist",
                    "status": "already_exists"
                }
            raise Exception(f"Database initialization failed: {e}")

    def get_all_attacks(self) -> List[Dict[str, Any]]:
        """Получение всех атак"""
        try:
            response = self.session.get(f"{self.base_url}/attacks")
            response.raise_for_status()

            data = response.json()

            if isinstance(data, dict) and 'data' in data:
                return data['data']
            elif isinstance(data, list):
                return data
            else:
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching attacks: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []

    def get_attack(self, attack_id: str) -> Dict[str, Any]:
        """Получение конкретной атаки"""
        try:
            response = self.session.get(f"{self.base_url}/attacks/{attack_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch attack {attack_id}: {e}")

    def create_attack(self, attack_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание новой атаки"""
        try:
            response = self.session.post(
                f"{self.base_url}/attacks",
                json=attack_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create attack: {e}")

    def update_attack(self, attack_id: str, attack_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление атаки (без целей)"""
        try:
            response = self.session.put(
                f"{self.base_url}/attacks/{attack_id}",
                json=attack_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update attack {attack_id}: {e}")

    def update_attack_with_targets(self, attack_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление атаки с целями"""
        try:
            response = self.session.put(
                f"{self.base_url}/attacks/{attack_id}/with-targets",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update attack {attack_id} with targets: {e}")

    def update_attack_targets(self, attack_id: str, targets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Обновление только целей атаки"""
        try:
            response = self.session.put(
                f"{self.base_url}/attacks/{attack_id}/targets",
                json={"targets": targets}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update targets for attack {attack_id}: {e}")

    def update_target(self, target_id: str, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление конкретной цели"""
        try:
            response = self.session.put(
                f"{self.base_url}/targets/{target_id}",
                json=target_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update target {target_id}: {e}")

    def delete_attack(self, attack_id: str) -> Dict[str, Any]:
        """Удаление атаки"""
        try:
            response = self.session.delete(f"{self.base_url}/attacks/{attack_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to delete attack {attack_id}: {e}")

    def reset_database(self) -> Dict[str, Any]:
        """Сброс базы данных"""
        try:
            response = self.session.post(f"{self.base_url}/database/reset")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Database reset failed: {e}")