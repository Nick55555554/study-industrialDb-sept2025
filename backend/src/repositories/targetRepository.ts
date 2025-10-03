import { db } from '../db';
import { Target, CreateTargetRequest, UpdateTargetRequest, Protocol } from '../models';
import { dbLogger } from '../logger';

export class TargetRepository {
    async create(targetData: Omit<Target, 'id' | 'created_at'>): Promise<Target> {
        try {
            dbLogger.debug('Creating new target', {
                targetIp: targetData.target_ip,
                attackId: targetData.attack_id
            });

            const [target] = await db('targets')
                .insert({
                    ...targetData,
                    tags: targetData.tags || [],
                    created_at: new Date()
                })
                .returning('*');

            dbLogger.debug('Target created successfully', {
                targetId: target.id,
                targetIp: target.target_ip
            });

            return target;
        } catch (error: any) {
            dbLogger.error('Error creating target', {
                error: error.message,
                targetData: {
                    targetIp: targetData.target_ip,
                    attackId: targetData.attack_id
                }
            });
            throw error;
        }
    }

    async createMultiple(targetsData: Omit<Target, 'id' | 'created_at'>[]): Promise<Target[]> {
        try {
            dbLogger.debug('Creating multiple targets', { count: targetsData.length });

            const dataWithTimestamp = targetsData.map(target => ({
                ...target,
                tags: target.tags || [],
                created_at: new Date()
            }));

            const targets = await db('targets')
                .insert(dataWithTimestamp)
                .returning('*');

            dbLogger.debug('Multiple targets created successfully', {
                count: targets.length
            });

            return targets;
        } catch (error: any) {
            dbLogger.error('Error creating multiple targets', {
                error: error.message,
                targetsCount: targetsData.length
            });
            throw error;
        }
    }

    async update(id: string, targetData: UpdateTargetRequest): Promise<Target | null> {
        try {
            dbLogger.info('Updating target', { targetId: id, updates: targetData });

            const [updatedTarget] = await db('targets')
                .where({ id })
                .update(targetData)
                .returning('*');

            if (updatedTarget) {
                dbLogger.info('Target updated successfully', { targetId: id });
            } else {
                dbLogger.warn('Target not found for update', { targetId: id });
            }

            return updatedTarget || null;
        } catch (error: any) {
            dbLogger.error('Error updating target', {
                targetId: id,
                error: error.message,
                updates: targetData
            });
            return null;
        }
    }

    async updateMultiple(targetsData: Array<{ id: string } & UpdateTargetRequest>): Promise<Target[]> {
        return await db.transaction(async (trx) => {
            try {
                dbLogger.debug('Updating multiple targets', { count: targetsData.length });

                const updatedTargets = [];

                for (const targetData of targetsData) {
                    const { id, ...updateData } = targetData;
                    const [updatedTarget] = await trx('targets')
                        .where({ id })
                        .update(updateData)
                        .returning('*');

                    if (updatedTarget) {
                        updatedTargets.push(updatedTarget);
                    }
                }

                dbLogger.debug('Multiple targets updated successfully', {
                    count: updatedTargets.length
                });

                return updatedTargets;
            } catch (error: any) {
                dbLogger.error('Error updating multiple targets', {
                    error: error.message,
                    targetsCount: targetsData.length
                });
                throw error;
            }
        });
    }

    async findByAttackId(attackId: string): Promise<Target[]> {
        try {
            dbLogger.debug('Finding targets by attack ID', { attackId });
            const targets = await db('targets').where({ attack_id: attackId });
            dbLogger.debug('Found targets by attack ID', {
                attackId,
                count: targets.length
            });
            return targets;
        } catch (error: any) {
            dbLogger.error('Error finding targets by attack ID', {
                attackId,
                error: error.message
            });
            throw error;
        }
    }

    async deleteByAttackId(attackId: string): Promise<boolean> {
        try {
            dbLogger.info('Deleting targets by attack ID', { attackId });
            const result = await db('targets').where({ attack_id: attackId }).delete();
            const success = result > 0;

            if (success) {
                dbLogger.info('Targets deleted successfully by attack ID', {
                    attackId,
                    deletedCount: result
                });
            } else {
                dbLogger.debug('No targets found for deletion by attack ID', { attackId });
            }

            return success;
        } catch (error: any) {
            dbLogger.error('Error deleting targets by attack ID', {
                attackId,
                error: error.message
            });
            return false;
        }
    }
}