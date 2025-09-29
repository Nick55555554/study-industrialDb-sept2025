import { db } from '../db'
import { AttackRepository } from '../repositories/attackRepository';
import { TargetRepository } from '../repositories/targetRepository';
import { Attack, CreateAttackRequest, AttackWithTargets, Target } from '../models';

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
                attack_type: attackData.attack_type
            });

            // Создаем цели если они есть
            let targets: Target[] = [];
            if (attackData.targets && attackData.targets.length > 0) {
                const targetsData = attackData.targets.map(target => ({
                    attack_id: attack.id,
                    target_ip: target.target_ip,
                    target_domain: target.target_domain,
                    port: target.port,
                    protocol: target.protocol
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

    async deleteAttack(attackId: string): Promise<boolean> {
        // Каскадное удаление сработает автоматически благодаря foreign key
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
        } catch (error) {
            console.error('Database initialization error:', error);
            return {
                success: false,
                message: `Failed to create tables: ${error}`
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
        } catch (error) {
            console.error('Database reset error:', error);
            return {
                success: false,
                message: `Failed to reset database: ${String(error)}`
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
                attacksCount = await db('ddos_attacks').count('id as count').first().then((result: any) => parseInt(result.count));
                targetsCount = await db('targets').count('id as count').first().then((result: any) => parseInt(result.count));
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