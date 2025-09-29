export interface Target {
    id: string;
    attack_id: string;
    target_ip: string;
    target_domain?: string;
    port?: number;
    protocol?: string;
    created_at: Date;
}

export interface CreateTargetRequest {
    target_ip: string;
    target_domain?: string;
    port?: number;
    protocol?: string;
}