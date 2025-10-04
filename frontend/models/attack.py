from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
from utils.helpers import generate_id, get_current_timestamp


@dataclass
class Target:
    target_ip: str = ""
    target_domain: str = ""
    port: int = 80
    protocol: str = "tcp"
    tags: List[str] = field(default_factory=list)


@dataclass
class Attack:
    name: str
    frequency: str = "high"
    danger: str = "high"
    attack_type: str = "amplification"
    source_ips: List[str] = field(default_factory=list)
    affected_ports: List[int] = field(default_factory=list)
    mitigation_strategies: List[str] = field(default_factory=list)
    targets: List[Target] = field(default_factory=list)
    id: str = field(default_factory=generate_id)
    created_at: str = field(default_factory=get_current_timestamp)
    updated_at: str = field(default_factory=get_current_timestamp)

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь для сохранения"""
        return {
            "id": self.id,
            "name": self.name,
            "frequency": self.frequency,
            "danger": self.danger,
            "attack_type": self.attack_type,
            "source_ips": self.source_ips,
            "affected_ports": self.affected_ports,
            "mitigation_strategies": self.mitigation_strategies,
            "targets": [target.__dict__ for target in self.targets],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Attack':
        """Создание объекта из словаря"""
        attack = cls(
            name=data["name"],
            frequency=data["frequency"],
            danger=data["danger"],
            attack_type=data["attack_type"],
            source_ips=data["source_ips"],
            affected_ports=data["affected_ports"],
            mitigation_strategies=data["mitigation_strategies"],
            id=data["id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )

        # Конвертация targets
        attack.targets = [
            Target(
                target_ip=target_data.get("target_ip", ""),
                target_domain=target_data.get("target_domain", ""),
                port=target_data.get("port", 80),
                protocol=target_data.get("protocol", "tcp"),
                tags=target_data.get("tags", [])
            ) for target_data in data.get("targets", [])
        ]

        return attack