import requests
import json
from typing import List, Dict, Any, Optional

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
            return {"success": False, "data": {"tablesExist": False}}

    def initialize_database(self) -> Dict[str, Any]:
        """Создание таблиц"""
        try:
            response = self.session.post(f"{self.base_url}/database/init")
            if response.status_code == 409:
                return {
                    "success": True,
                    "message": "Tables already exist",
                    "status": "already_exists"
                }
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if "409" in str(e):
                return {
                    "success": True,
                    "message": "Tables already exist",
                    "status": "already_exists"
                }
            raise Exception(f"Database initialization failed: {e}")

    def filter_attacks_by_frequency(self, frequencies: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по частоте"""
        try:
            if not frequencies:
                return self.get_all_attacks()

            frequency_param = ",".join(frequencies)
            response = self.session.get(
                f"{self.base_url}/attacks/filter",
                params={"frequency": frequency_param}
            )
            response.raise_for_status()
            data = response.json()
            return self._extract_attacks_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Filter by frequency error: {e}")
            return []

    def filter_attacks_by_danger(self, danger_levels: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по уровню опасности"""
        try:
            if not danger_levels:
                return self.get_all_attacks()

            danger_param = ",".join(danger_levels)
            response = self.session.get(
                f"{self.base_url}/attacks/filter",
                params={"danger": danger_param}
            )
            response.raise_for_status()
            data = response.json()
            return self._extract_attacks_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Filter by danger error: {e}")
            return []

    def filter_attacks_by_attack_type(self, attack_types: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по типу атаки"""
        try:
            if not attack_types:
                return self.get_all_attacks()

            attack_type_param = ",".join(attack_types)
            response = self.session.get(
                f"{self.base_url}/attacks/filter",
                params={"attack_type": attack_type_param}
            )
            response.raise_for_status()
            data = response.json()
            return self._extract_attacks_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Filter by attack type error: {e}")
            return []

    def filter_attacks_by_protocol(self, protocols: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по протоколу"""
        try:
            if not protocols:
                return self.get_all_attacks()

            protocol_param = ",".join(protocols)
            response = self.session.get(
                f"{self.base_url}/attacks/filter",
                params={"protocol": protocol_param}
            )
            response.raise_for_status()
            data = response.json()
            return self._extract_attacks_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Filter by protocol error: {e}")
            return []

    def filter_attacks_by_multiple(self, frequencies: Optional[List[str]] = None,
                                   danger_levels: Optional[List[str]] = None,
                                   attack_types: Optional[List[str]] = None,
                                   protocols: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Фильтрация атак по нескольким параметрам"""
        try:
            params = {}

            if frequencies:
                params["frequency"] = ",".join(frequencies)

            if danger_levels:
                params["danger"] = ",".join(danger_levels)

            if attack_types:
                params["attack_type"] = ",".join(attack_types)

            if protocols:
                params["protocol"] = ",".join(protocols)

            if not params:
                return self.get_all_attacks()

            response = self.session.get(
                f"{self.base_url}/attacks/filter",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            return self._extract_attacks_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Filter by multiple error: {e}")
            return []

    def _extract_attacks_data(self, data: Any) -> List[Dict[str, Any]]:
        """Извлекает данные об атаках из ответа сервера"""
        if isinstance(data, dict):
            if 'data' in data:
                return data['data']
            elif 'attacks' in data:
                return data['attacks']
            else:
                return []
        elif isinstance(data, list):
            valid_attacks = []
            for item in data:
                if isinstance(item, dict):
                    valid_attacks.append(item)
                else:
                    print(f"Warning: Skipping non-dict item in attacks list: {item}")
            return valid_attacks
        else:
            print(f"Warning: Unexpected data format from server: {type(data)}")
            return []

    def get_all_attacks(self) -> List[Dict[str, Any]]:
        """Получение всех атак"""
        try:
            response = self.session.get(f"{self.base_url}/attacks")
            response.raise_for_status()
            data = response.json()
            return self._extract_attacks_data(data)
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