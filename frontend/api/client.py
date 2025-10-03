import requests
import json
from typing import List, Dict, Any, Optional
from models.attack import Attack


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
            raise Exception(f"Database status check failed: {e}")

    def initialize_database(self) -> Dict[str, Any]:
        """Создание таблиц"""
        try:
            response = self.session.post(f"{self.base_url}/database/init")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Database initialization failed: {e}")

    def get_all_attacks(self) -> List[Dict[str, Any]]:
        """Получение всех атак"""
        try:
            response = self.session.get(f"{self.base_url}/attacks")
            response.raise_for_status()

            # Добавьте отладку
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")

            data = response.json()

            # Проверяем структуру ответа
            if isinstance(data, dict) and 'data' in data:
                # Если ответ в формате {success: true, data: [...]}
                return data['data']
            elif isinstance(data, list):
                # Если ответ сразу массив
                return data
            else:
                print(f"Unexpected response format: {data}")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise Exception(f"Failed to fetch attacks: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response.text}")
            raise Exception(f"Invalid JSON response: {e}")

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