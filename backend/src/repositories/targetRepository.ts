import { db } from '../db';
import { Target, CreateTargetRequest, UpdateTargetRequest, Protocol } from '../models';

export class TargetRepository {
    async create(targetData: Omit<Target, 'id' | 'created_at'>): Promise<Target> {
        const [target] = await db('targets')
            .insert({
                ...targetData,
                tags: targetData.tags || [],
                created_at: new Date()
            })
            .returning('*');

        return target;
    }

    async createMultiple(targetsData: Omit<Target, 'id' | 'created_at'>[]): Promise<Target[]> {
        const dataWithTimestamp = targetsData.map(target => ({
            ...target,
            tags: target.tags || [],
            created_at: new Date()
        }));

        return await db('targets')
            .insert(dataWithTimestamp)
            .returning('*');
    }

    async update(id: string, targetData: UpdateTargetRequest): Promise<Target | null> {
        try {
            const [updatedTarget] = await db('targets')
                .where({ id })
                .update(targetData)
                .returning('*');

            return updatedTarget || null;
        } catch (error) {
            console.error('Error updating target:', error);
            return null;
        }
    }

    async updateMultiple(targetsData: Array<{ id: string } & UpdateTargetRequest>): Promise<Target[]> {
        return await db.transaction(async (trx) => {
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

            return updatedTargets;
        });
    }

    async findByAttackId(attackId: string): Promise<Target[]> {
        return await db('targets').where({ attack_id: attackId });
    }

    async deleteByAttackId(attackId: string): Promise<boolean> {
        const result = await db('targets').where({ attack_id: attackId }).delete();
        return result > 0;
    }
}