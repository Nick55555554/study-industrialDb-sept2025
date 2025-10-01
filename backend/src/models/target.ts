import { Protocol } from './attack';

export interface Target {
    id: string;
    attack_id: string;
    target_ip: string;
    target_domain?: string;
    port?: number;
    protocol?: Protocol;
    tags: string[]; // Массив тегов для цели
    created_at: Date;
}

export interface CreateTargetRequest {
    target_ip: string;
    target_domain?: string;
    port?: number;
    protocol?: Protocol;
    tags?: string[];
}

export interface UpdateTargetRequest {
    target_ip?: string;
    target_domain?: string;
    port?: number;
    protocol?: Protocol;
    tags?: string[];
}