import { db } from '../db';
import { AttackRepository } from '../repositories/attackRepository';
import { TargetRepository } from '../repositories/targetRepository';
import {
    Attack,
    Target,
    CreateAttackRequest,
    AttackWithTargets,
    UpdateAttackRequest,
    UpdateTargetRequest,
    AttackFilter,
    AttackStats,
    AttackFrequency,
    AttackDanger,
    AttackType,
    Protocol
} from '../models';
import { appLogger, errorLogger } from '../logger';

export class AttackService {
    private attackRepository: AttackRepository;
    private targetRepository: TargetRepository;

    constructor() {
        this.attackRepository = new AttackRepository();
        this.targetRepository = new TargetRepository();
        appLogger.info('AttackService initialized');
    }

    async createAttackWithTargets(attackData: CreateAttackRequest): Promise<AttackWithTargets> {
        try {
            appLogger.info('Creating attack with targets', {
                name: attackData.name,
                targetsCount: attackData.targets?.length || 0
            });

            const result = await db.transaction(async (trx) => {
                const attack = await this.attackRepository.create({
                    name: attackData.name,
                    frequency: attackData.frequency,
                    danger: attackData.danger,
                    attack_type: attackData.attack_type,
                    source_ips: attackData.source_ips || [],
                    affected_ports: attackData.affected_ports || [],
                    mitigation_strategies: attackData.mitigation_strategies || []
                });

                let targets:Target[] = [];
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

            appLogger.info('Attack with targets created successfully', {
                attackId: result.id,
                name: result.name,
                targetsCount: result.targets.length
            });

            return result;
        } catch (error: any) {
            errorLogger.error('Error creating attack with targets', {
                attackData: {
                    name: attackData.name,
                    type: attackData.attack_type
                },
                error: error.message,
                stack: error.stack
            });
            throw new Error(`Failed to create attack with targets: ${error.message}`);
        }
    }

    async getAttackWithTargets(attackId: string): Promise<AttackWithTargets | null> {
        try {
            appLogger.debug('Getting attack with targets', { attackId });

            const attack = await this.attackRepository.findById(attackId);
            if (!attack) {
                appLogger.debug('Attack not found for getting with targets', { attackId });
                return null;
            }

            const targets = await this.targetRepository.findByAttackId(attackId);

            appLogger.debug('Attack with targets retrieved successfully', {
                attackId,
                targetsCount: targets.length
            });

            return {
                ...attack,
                targets
            };
        } catch (error: any) {
            errorLogger.error('Error getting attack with targets', {
                attackId,
                error: error.message
            });
            throw new Error(`Failed to get attack with targets: ${error.message}`);
        }
    }

    async getAllAttacks(): Promise<Attack[]> {
        try {
            appLogger.debug('Getting all attacks');
            const attacks = await this.attackRepository.findAll();
            appLogger.debug('All attacks retrieved successfully', { count: attacks.length });
            return attacks;
        } catch (error: any) {
            errorLogger.error('Error getting all attacks', { error: error.message });
            throw new Error(`Failed to get all attacks: ${error.message}`);
        }
    }

    async updateAttack(attackId: string, attackData: UpdateAttackRequest): Promise<Attack | null> {
        try {
            appLogger.info('Updating attack', { attackId, updates: attackData });

            const updatedAttack = await this.attackRepository.update(attackId, attackData);

            if (updatedAttack) {
                appLogger.info('Attack updated successfully', { attackId });
            } else {
                appLogger.warn('Attack not found for update', { attackId });
            }

            return updatedAttack;
        } catch (error: any) {
            errorLogger.error('Error updating attack', {
                attackId,
                error: error.message,
                updates: attackData
            });
            throw new Error(`Failed to update attack: ${error.message}`);
        }
    }

    async updateAttackWithTargets(attackId: string, attackData: UpdateAttackRequest, targetsData?: UpdateTargetRequest[]): Promise<AttackWithTargets | null> {
        try {
            appLogger.info('Updating attack with targets', {
                attackId,
                targetsCount: targetsData?.length || 0
            });

            const result = await this.attackRepository.updateWithTargets(attackId, attackData, targetsData);

            if (result) {
                appLogger.info('Attack with targets updated successfully', {
                    attackId,
                    targetsCount: result.targets.length
                });
            } else {
                appLogger.warn('Attack not found for update with targets', { attackId });
            }

            return result;
        } catch (error: any) {
            errorLogger.error('Error updating attack with targets', {
                attackId,
                error: error.message,
                stack: error.stack
            });
            throw new Error(`Failed to update attack with targets: ${error.message}`);
        }
    }

    async updateTarget(targetId: string, targetData: UpdateTargetRequest): Promise<Target | null> {
        try {
            appLogger.info('Updating target', { targetId, updates: targetData });

            const updatedTarget = await this.targetRepository.update(targetId, targetData);

            if (updatedTarget) {
                appLogger.info('Target updated successfully', { targetId });
            } else {
                appLogger.warn('Target not found for update', { targetId });
            }

            return updatedTarget;
        } catch (error: any) {
            errorLogger.error('Error updating target', {
                targetId,
                error: error.message,
                updates: targetData
            });
            throw new Error(`Failed to update target: ${error.message}`);
        }
    }

    async updateAttackTargets(attackId: string, targetsData: UpdateTargetRequest[]): Promise<Target[]> {
        try {
            appLogger.info('Updating attack targets', { attackId, targetsCount: targetsData.length });

            await this.targetRepository.deleteByAttackId(attackId);

            if (targetsData.length === 0) {
                appLogger.debug('No targets to create after deletion', { attackId });
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

            const createdTargets = await this.targetRepository.createMultiple(targetsToCreate);

            appLogger.info('Attack targets updated successfully', {
                attackId,
                targetsCount: createdTargets.length
            });

            return createdTargets;
        } catch (error: any) {
            errorLogger.error('Error updating attack targets', {
                attackId,
                error: error.message,
                stack: error.stack
            });
            throw new Error(`Failed to update attack targets: ${error.message}`);
        }
    }

    async deleteAttack(attackId: string): Promise<boolean> {
        try {
            appLogger.info('Deleting attack', { attackId });

            const success = await this.attackRepository.delete(attackId);

            if (success) {
                appLogger.info('Attack deleted successfully', { attackId });
            } else {
                appLogger.warn('Attack not found for deletion', { attackId });
            }

            return success;
        } catch (error: any) {
            errorLogger.error('Error deleting attack', {
                attackId,
                error: error.message
            });
            throw new Error(`Failed to delete attack: ${error.message}`);
        }
    }

    async initializeDatabase(): Promise<{ success: boolean; message: string }> {
        try {
            appLogger.info('Initializing database');

            const tablesExist = await this.attackRepository.checkTablesExist();

            if (tablesExist) {
                appLogger.info('Database tables already exist');
                return {
                    success: false,
                    message: 'Tables already exist'
                };
            }

            await this.attackRepository.createTables();

            appLogger.info('Database initialized successfully');
            return {
                success: true,
                message: 'Tables created successfully'
            };
        } catch (error: any) {
            errorLogger.error('Database initialization error', {
                error: error.message,
                stack: error.stack
            });
            const errorMessage = error?.message || String(error);
            return {
                success: false,
                message: `Failed to create tables: ${errorMessage}`
            };
        }
    }

    async resetDatabase(): Promise<{ success: boolean; message: string }> {
        try {
            appLogger.info('Resetting database');

            await this.attackRepository.dropTables();
            await this.attackRepository.createTables();

            appLogger.info('Database reset successfully');
            return {
                success: true,
                message: 'Database reset successfully'
            };
        } catch (error: any) {
            errorLogger.error('Database reset error', {
                error: error.message,
                stack: error.stack
            });
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
            appLogger.debug('Getting database status');

            const tablesExist = await this.attackRepository.checkTablesExist();
            let attacksCount = 0;
            let targetsCount = 0;

            if (tablesExist) {
                const attacksResult = await db('ddos_attacks').count('id as count').first();
                const targetsResult = await db('targets').count('id as count').first();

                attacksCount = parseInt(attacksResult?.count as string) || 0;
                targetsCount = parseInt(targetsResult?.count as string) || 0;
            }

            appLogger.debug('Database status retrieved', {
                tablesExist,
                attacksCount,
                targetsCount
            });

            return {
                tablesExist,
                attacksCount,
                targetsCount
            };
        } catch (error: any) {
            errorLogger.error('Database status check error', { error: error.message });
            return {
                tablesExist: false,
                attacksCount: 0,
                targetsCount: 0
            };
        }
    }

    async getAttacksByFilters(filters: AttackFilter): Promise<Attack[]> {
        try {
            appLogger.debug('Getting attacks by filters', { filters });

            const attacks = await this.attackRepository.findByFilters(filters);

            appLogger.debug('Retrieved attacks by filters', {
                filter: filters,
                count: attacks.length
            });

            return attacks;
        } catch (error: any) {
            errorLogger.error('Error getting attacks by filters', {
                filters,
                error: error.message,
                stack: error.stack
            });
            throw new Error(`Failed to get attacks by filters: ${error.message}`);
        }
    }

    async getAttackStats(): Promise<AttackStats> {
        try {
            appLogger.debug('Getting attack statistics');
            const stats = await this.attackRepository.getStats();
            appLogger.debug('Attack statistics retrieved successfully');
            return stats;
        } catch (error: any) {
            errorLogger.error('Error getting attack stats', { error: error.message });
            throw new Error(`Failed to get attack stats: ${error.message}`);
        }
    }

    async getAvailableFilters(): Promise<{
        frequencies: AttackFrequency[];
        dangers: AttackDanger[];
        attackTypes: AttackType[];
        protocols: Protocol[];
    }> {
        try {
            appLogger.debug('Getting available filters');
            const filters = await this.attackRepository.getAvailableFilters();
            appLogger.debug('Available filters retrieved successfully');
            return filters;
        } catch (error: any) {
            errorLogger.error('Error getting available filters', { error: error.message });
            throw new Error(`Failed to get available filters: ${error.message}`);
        }
    }

    async getAttacksByFrequency(frequency: AttackFrequency): Promise<Attack[]> {
        try {
            appLogger.debug('Getting attacks by frequency', { frequency });
            const attacks = await this.getAttacksByFilters({ frequency });
            appLogger.debug('Attacks by frequency retrieved', { frequency, count: attacks.length });
            return attacks;
        } catch (error: any) {
            errorLogger.error('Error getting attacks by frequency', { frequency, error: error.message });
            throw error;
        }
    }

    async getAttacksByDanger(danger: AttackDanger): Promise<Attack[]> {
        try {
            appLogger.debug('Getting attacks by danger', { danger });
            const attacks = await this.getAttacksByFilters({ danger });
            appLogger.debug('Attacks by danger retrieved', { danger, count: attacks.length });
            return attacks;
        } catch (error: any) {
            errorLogger.error('Error getting attacks by danger', { danger, error: error.message });
            throw error;
        }
    }

    async getAttacksByType(attackType: AttackType): Promise<Attack[]> {
        try {
            appLogger.debug('Getting attacks by type', { attackType });
            const attacks = await this.getAttacksByFilters({ attack_type: attackType });
            appLogger.debug('Attacks by type retrieved', { attackType, count: attacks.length });
            return attacks;
        } catch (error: any) {
            errorLogger.error('Error getting attacks by type', { attackType, error: error.message });
            throw error;
        }
    }

    async getAttacksByProtocol(protocol: Protocol): Promise<Attack[]> {
        try {
            appLogger.debug('Getting attacks by protocol', { protocol });
            const attacks = await this.getAttacksByFilters({ protocol });
            appLogger.debug('Attacks by protocol retrieved', { protocol, count: attacks.length });
            return attacks;
        } catch (error: any) {
            errorLogger.error('Error getting attacks by protocol', { protocol, error: error.message });
            throw error;
        }
    }
}