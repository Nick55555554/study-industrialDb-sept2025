import type {Knex} from 'knex';

import {Attack, type AttackData} from '../db/models/attack';
import { Rate } from '../types/rate';

export class SharedTicketFeedbackRepository {

    static async create( data: Omit<AttackData, 'id'>, trx: Knex) {
        const feedback = await Attack.query(trx).insert({
            ...data,
        });
        return feedback;
    
    }

    static async findByFrequency( frequency: Rate, trx: Knex) {
        const attacks = await Attack.findByFrequency(frequency, trx);
        return attacks;
    }

    static async findByDanger( danger: Rate, trx: Knex) {
        const attacks = await Attack.findByDanger(danger, trx)
        return attacks;
    }
}
