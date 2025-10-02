import { db } from '../db';
import { AttackRepository } from '../repositories/attackRepository';
import { TargetRepository } from '../repositories/targetRepository';
import {
    Attack,
    CreateAttackRequest,
    AttackWithTargets,
    UpdateAttackRequest,
    UpdateTargetRequest,
    AttackFrequency,
    AttackDanger,
    AttackType,
    Protocol,
    Target
} from '../models';

export class AttackService {
    private attackRepository: AttackRepository;
    private targetRepository: TargetRepository;

    constructor() {
        this.attackRepository = new AttackRepository();
        this.targetRepository = new TargetRepository();
    }

    async createAttackWithTargets(attackData: CreateAttackRequest): Promise<AttackWithTargets> {
        return await db.transaction(async (trx) => {
            // Создаем атаку
            const attack = await this.attackRepository.create({
                name: attackData.name,
                frequency: attackData.frequency,
                danger: attackData.danger,
                attack_type: attackData.attack_type,
                source_ips: attackData.source_ips || [],
                affected_ports: attackData.affected_ports || [],
                mitigation_strategies: attackData.mitigation_strategies || []
            });

            // Создаем цели если они есть
            let targets: Target[] = [];
            if (attackData.targets && attackData.targets.length > 0) {
                const targetsData = attackData.targets.map(target => ({
                    attack_id: attack.id,
                    target_ip: target.target_ip,
                    target_domain: target.target_domain,
                    port: target.port,
                    protocol: target.protocol,
                    tags: target.tags || []
                }));

                targets = await this.targetRepository.createMultiple(targetsData);
            }

            return {
                ...attack,
                targets
            };
        });
    }

    async getAttackWithTargets(attackId: string): Promise<AttackWithTargets | null> {
        const attack = await this.attackRepository.findById(attackId);
        if (!attack) return null;

        const targets = await this.targetRepository.findByAttackId(attackId);

        return {
            ...attack,
            targets
        };
    }

    async getAllAttacks(): Promise<Attack[]> {
        return await this.attackRepository.findAll();
    }

    async updateAttack(attackId: string, attackData: UpdateAttackRequest): Promise<Attack | null> {
        try {
            return await this.attackRepository.update(attackId, attackData);
        } catch (error: any) {
            console.error('Update attack error:', error);
            throw new Error(`Failed to update attack: ${error.message}`);
        }
    }

    async updateAttackWithTargets(attackId: string, attackData: UpdateAttackRequest, targetsData?: UpdateTargetRequest[]): Promise<AttackWithTargets | null> {
        try {
            return await this.attackRepository.updateWithTargets(attackId, attackData, targetsData);
        } catch (error: any) {
            console.error('Update attack with targets error:', error);
            throw new Error(`Failed to update attack with targets: ${error.message}`);
        }
    }

    async updateTarget(targetId: string, targetData: UpdateTargetRequest): Promise<Target | null> {
        try {
            return await this.targetRepository.update(targetId, targetData);
        } catch (error: any) {
            console.error('Update target error:', error);
            throw new Error(`Failed to update target: ${error.message}`);
        }
    }

    async updateAttackTargets(attackId: string, targetsData: UpdateTargetRequest[]): Promise<Target[]> {
        try {
            // Удаляем старые цели и создаем новые
            await this.targetRepository.deleteByAttackId(attackId);

            if (targetsData.length === 0) {
                return [];
            }

            const targetsToCreate = targetsData.map(target => ({
                attack_id: attackId,
                target_ip: target.target_ip!,
                target_domain: target.target_domain,
                port: target.port,
                protocol: target.protocol,
                tags: target.tags || []
            }));

            return await this.targetRepository.createMultiple(targetsToCreate);
        } catch (error: any) {
            console.error('Update attack targets error:', error);
            throw new Error(`Failed to update attack targets: ${error.message}`);
        }
    }

    async deleteAttack(attackId: string): Promise<boolean> {
        return await this.attackRepository.delete(attackId);
    }

    async initializeDatabase(): Promise<{ success: boolean; message: string }> {
        try {
            const tablesExist = await this.attackRepository.checkTablesExist();

            if (tablesExist) {
                return {
                    success: false,
                    message: 'Tables already exist'
                };
            }

            await this.attackRepository.createTables();

            return {
                success: true,
                message: 'Tables created successfully'
            };
        } catch (error: any) {
            console.error('Database initialization error:', error);
            const errorMessage = error?.message || String(error);
            return {
                success: false,
                message: `Failed to create tables: ${errorMessage}`
            };
        }
    }

    async resetDatabase(): Promise<{ success: boolean; message: string }> {
        try {
            await this.attackRepository.dropTables();
            await this.attackRepository.createTables();

            return {
                success: true,
                message: 'Database reset successfully'
            };
        } catch (error: any) {
            console.error('Database reset error:', error);
            const errorMessage = error?.message || String(error);
            return {
                success: false,
                message: `Failed to reset database: ${errorMessage}`
            };
        }
    }

    async getDatabaseStatus(): Promise<{
        tablesExist: boolean;
        attacksCount: number;
        targetsCount: number;
    }> {
        try {
            const tablesExist = await this.attackRepository.checkTablesExist();
            let attacksCount = 0;
            let targetsCount = 0;

            if (tablesExist) {
                const attacksResult = await db('ddos_attacks').count('id as count').first();
                const targetsResult = await db('targets').count('id as count').first();

                attacksCount = parseInt(attacksResult?.count as string) || 0;
                targetsCount = parseInt(targetsResult?.count as string) || 0;
            }

            return {
                tablesExist,
                attacksCount,
                targetsCount
            };
        } catch (error) {
            console.error('Database status check error:', error);
            return {
                tablesExist: false,
                attacksCount: 0,
                targetsCount: 0
            };
        }
    }
}