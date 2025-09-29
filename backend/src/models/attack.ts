import { Rate } from "../types/rate";
import { TypesOfAttack } from "../types/type-of-attack";
import { Target, CreateTargetRequest } from './target'

export interface Attack {
    id: string;
    name: string;
    frequency: string;
    danger: string;
    attack_type: string;
    created_at: Date;
    updated_at: Date;
}

export interface CreateAttackRequest {
    name: string;
    frequency: string;
    danger: string;
    attack_type: string;
    targets?: CreateTargetRequest[];
}

export interface AttackWithTargets extends Attack {
    targets: Target[];
}
