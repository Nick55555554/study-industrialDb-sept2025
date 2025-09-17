import type {Knex} from 'knex';

import {Attack, type AttackData} from '../db/models/attack';
import { Rate } from '../types/rate';
import { TypesOfAttack} from '../types/type-of-attack'
import { query } from 'express';

export class AttackRepository {

    static async create( data: Omit<AttackData, 'id'>, trx: Knex) {
        const feedback = await Attack.query(trx).insert({
            ...data,
        });
        return feedback;

    }

    static async createAttack(name: string,
            frequency: Rate,
            danger: Rate,
            attackType: TypesOfAttack,
            trx: Knex){
                const attack = await Attack.createAttack(name, frequency, danger, attackType, trx);
                return attack;
            }

    static async findByFrequency( frequency: Rate, trx: Knex) {
        const attacks = await Attack.findByFrequency(frequency, trx);
        return attacks;
    }

    static async findByDanger( danger: Rate, trx: Knex) {
        const attacks = await Attack.findByDanger(danger, trx)
        return attacks;
    }

    static async delById(id: string, trx: Knex){
        const feedback = await Attack.query(trx)
        .where('id', id)
        .del();
    }
    static async update(
        id: string,
        updateData: Partial<Omit<AttackData, 'id' | 'createdAt'>>,
        trx?: any
    ){
        return Attack.updateAttack(id, updateData, trx);
    }

    static async findAllAttacks(trx : Knex){
        const feedback = await Attack.query(trx).select('*').orderBy('name');
        return feedback;
    }
}
