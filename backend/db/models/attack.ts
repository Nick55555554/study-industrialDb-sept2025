import { Model } from './base-model';
import { Rate } from '../../types/rate';

export interface AttackData {
    id: string;
    name: string;
    frequency: Rate;
    danger: Rate;
}

export class Attack extends Model implements AttackData {
    static readonly tableName = 'ticket_links';
    static readonly idColumn = 'id';

    static async findByFrequency(frequency: Rate, trx?: any) {
        return this.query(trx)
        .where('frequency', frequency)
        .select('*');
    }

    static async findByDanger(danger: Rate, trx?: any) {
        return this.query(trx)
        .where('danger', danger)
        .orderBy('name');
    }


    id!: AttackData['id'];
    name!: AttackData['name'];
    frequency!: AttackData['frequency'];
    danger!: AttackData['danger'];
}