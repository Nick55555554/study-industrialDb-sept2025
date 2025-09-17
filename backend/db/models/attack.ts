import { Model } from './base-model';
import { Rate } from '../../types/rate';
import { TypesOfAttack } from '../../types/type-of-attack';


export interface AttackData {
    id: string;
    name: string;
    frequency: Rate;
    danger: Rate;
    attackType: TypesOfAttack;
}

export class Attack extends Model implements AttackData {
    static readonly tableName = 'ticket_links';
    static readonly idColumn = 'id';

    static async createAttack(
        name: string,
        frequency: Rate,
        danger: Rate,
        attackType: TypesOfAttack,
        trx?: any){
        return this.query(trx)
        .insert({
            name,
            frequency,
            danger,
            attack_type: attackType
        })
        .returning('*');
    }

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

    static async findById(id: string, trx?: any){
        return this.query(trx)
        .where('id', id)
        .first()
    }

    static async updateAttack(
    id: string,
    updateData: Partial<AttackData>,
    trx?: any
) {
    return this.query(trx)
        .where({ id })
        .update({
            ...updateData,
        })
        .returning('*');
}

    //поля класса для TS
    id!: AttackData['id'];
    name!: AttackData['name'];
    frequency!: AttackData['frequency'];
    danger!: AttackData['danger'];
    attackType!: AttackData['attackType'];
    //доп поле для БД
    attack_type!: TypesOfAttack;

}