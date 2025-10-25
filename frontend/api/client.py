from typing import List, Dict, Any, Optional
from .db_manager import DatabaseManager


class DDOSDatabaseClient:
    def __init__(self):
        # Для PostgreSQL убираем параметр db_path
        self.db = DatabaseManager()

    def check_database_status(self) -> Dict[str, Any]:
        """Проверка статуса БД"""
        return self.db.check_database_status()

    def initialize_database(self) -> Dict[str, Any]:
        """Создание таблиц"""
        return self.db.initialize_database()

    def get_all_attacks(self) -> List[Dict[str, Any]]:
        """Получение всех атак"""
        return self.db.get_all_attacks()

    def get_attack(self, attack_id: str) -> Dict[str, Any]:
        """Получение конкретной атаки"""
        result = self.db.get_attack(attack_id)
        if result is None:
            raise Exception(f"Attack {attack_id} not found")
        return result

    def create_attack(self, attack_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание новой атаки"""
        return self.db.create_attack(attack_data)

    def update_attack(self, attack_id: str, attack_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление атаки"""
        return self.db.update_attack(attack_id, attack_data)

    def update_attack_with_targets(self, attack_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление атаки с целями"""
        return self.db.update_attack_with_targets(attack_id, data)

    def update_attack_targets(self, attack_id: str, targets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Обновление только целей атаки"""
        # Получаем текущую атаку
        current_attack = self.db.get_attack(attack_id)
        if not current_attack:
            raise Exception(f"Attack {attack_id} not found")

        # Обновляем только цели
        update_data = {
            "name": current_attack["name"],
            "frequency": current_attack["frequency"],
            "danger": current_attack["danger"],
            "attack_type": current_attack["attack_type"],
            "source_ips": current_attack["source_ips"],
            "affected_ports": current_attack["affected_ports"],
            "mitigation_strategies": current_attack["mitigation_strategies"],
            "targets": targets
        }

        return self.db.update_attack_with_targets(attack_id, update_data)

    def update_target(self, target_id: str, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление конкретной цели"""
        return self.db.update_target(int(target_id), target_data)

    def delete_attack(self, attack_id: str) -> Dict[str, Any]:
        """Удаление атаки"""
        return self.db.delete_attack(attack_id)

    def reset_database(self) -> Dict[str, Any]:
        """Сброс базы данных"""
        return self.db.reset_database()

    # Методы фильтрации
    def filter_attacks_by_frequency(self, frequencies: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по частоте"""
        if not frequencies:
            return self.get_all_attacks()
        return self.db.filter_attacks(frequencies=frequencies)

    def filter_attacks_by_danger(self, danger_levels: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по уровню опасности"""
        if not danger_levels:
            return self.get_all_attacks()
        return self.db.filter_attacks(danger_levels=danger_levels)

    def filter_attacks_by_attack_type(self, attack_types: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по типу атаки"""
        if not attack_types:
            return self.get_all_attacks()
        return self.db.filter_attacks(attack_types=attack_types)

    def filter_attacks_by_protocol(self, protocols: List[str]) -> List[Dict[str, Any]]:
        """Фильтрация атак по протоколу"""
        if not protocols:
            return self.get_all_attacks()
        return self.db.filter_attacks(protocols=protocols)

    def filter_attacks_by_multiple(self, frequencies: Optional[List[str]] = None,
                                   danger_levels: Optional[List[str]] = None,
                                   attack_types: Optional[List[str]] = None,
                                   protocols: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Фильтрация атак по нескольким параметрам"""
        return self.db.filter_attacks(
            frequencies=frequencies,
            danger_levels=danger_levels,
            attack_types=attack_types,
            protocols=protocols
        )

    def _extract_attacks_data(self, data: Any) -> List[Dict[str, Any]]:
        """Совместимость со старым API клиентом"""
        if isinstance(data, dict) and 'data' in data:
            return data['data']
        elif isinstance(data, list):
            return data
        else:
            return []