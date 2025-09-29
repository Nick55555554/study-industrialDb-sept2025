import { db } from '../db';
import { Target, CreateTargetRequest } from '../models';

export class TargetRepository {
    async create(targetData: Omit<Target, 'id' | 'created_at'>): Promise<Target> {
        const [target] = await db('targets')
            .insert({
                ...targetData,
                created_at: new Date()
            })
            .returning('*');
        return target;
    }

    async createMultiple(targetsData: Omit<Target, 'id' | 'created_at'>[]): Promise<Target[]> {
        const dataWithTimestamp = targetsData.map(target => ({
            ...target,
            created_at: new Date()
        }));

        return await db('targets')
            .insert(dataWithTimestamp)
            .returning('*');
    }

    async findByAttackId(attackId: string): Promise<Target[]> {
        return await db('targets').where({ attack_id: attackId });
    }

    async deleteByAttackId(attackId: string): Promise<boolean> {
        const result = await db('targets').where({ attack_id: attackId }).delete();
        return result > 0;
    }
}