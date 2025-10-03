import uuid
from datetime import datetime
from typing import List, Dict, Any





class Attack:
    class Target:
        def __init__(self, target_id: str, ip_address: str, protocol: str, status: str = "active"):
            self.target_id = target_id
            self.ip_address = ip_address
            self.protocol = protocol
            self.status = status

        def to_dict(self) -> Dict[str, Any]:
            return {
                "target_id": self.target_id,
                "ip_address": self.ip_address,
                "protocol": self.protocol,
                "status": self.status
            }

    def __init__(self, attack_id: str, name: str, frequency: str, danger: str, 
                 attack_type: str, source_ips: List[str], affected_ports: List[int],
                 mitigation_strategies: List[str], targets: List[Target]):
        self.attack_id = attack_id
        self.name = name
        self.frequency = frequency
        self.danger = danger
        self.attack_type = attack_type
        self.source_ips = source_ips
        self.affected_ports = affected_ports
        self.mitigation_strategies = mitigation_strategies
        self.targets = targets
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attack_id": self.attack_id,
            "name": self.name,
            "frequency": self.frequency,
            "danger": self.danger,
            "attack_type": self.attack_type,
            "source_ips": self.source_ips,
            "affected_ports": self.affected_ports,
            "mitigation_strategies": self.mitigation_strategies,
            "targets": [target.to_dict() for target in self.targets],
            "created_at": self.created_at
        }