import { Target, CreateTargetRequest } from "./target";

export enum AttackFrequency {
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high",
    VERY_HIGH = "very_high",
}

export enum AttackDanger {
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high",
    CRITICAL = "critical",
}

export enum AttackType {
    VOLUMETRIC = "volumetric",
    PROTOCOL = "protocol",
    APPLICATION = "application",
    AMPLIFICATION = "amplification",
}

export enum Protocol {
    HTTP = "http",
    HTTPS = "https",
    TCP = "tcp",
    UDP = "udp",
    SSH = "ssh",
    DNS = "dns",
}

export interface Attack {
    id: string;
    name: string;
    frequency: AttackFrequency;
    danger: AttackDanger;
    attack_type: AttackType;
    source_ips: string[]; // Массив IP адресов источников
    affected_ports: number[]; // Массив затронутых портов
    mitigation_strategies: string[]; // Массив стратегий защиты
    created_at: Date;
    updated_at: Date;
}

export interface CreateAttackRequest {
    name: string;
    frequency: AttackFrequency;
    danger: AttackDanger;
    attack_type: AttackType;
    source_ips?: string[];
    affected_ports?: number[];
    mitigation_strategies?: string[];
    targets?: CreateTargetRequest[];
}

export interface UpdateAttackRequest {
    name?: string;
    frequency?: AttackFrequency;
    danger?: AttackDanger;
    attack_type?: AttackType;
    source_ips?: string[];
    affected_ports?: number[];
    mitigation_strategies?: string[];
}

export interface AttackWithTargets extends Attack {
    targets: Target[];
}
