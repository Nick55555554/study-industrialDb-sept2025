import type { Knex } from "knex";

import { Attack, type AttackData } from "../db/models/attack";

export class AttackRepository {
    static async create(data: Omit<AttackData, "id">, trx: Knex) {
        return Attack.query(trx).insert(data).returning("*");
    }

    static async delById(id: string, trx: Knex) {
        const result = await Attack.query(trx).where("id", id).del();
        if (result === 0) {
            throw new Error("Attack not found");
        }
        return result;
    }

    static async update(
        id: string,
        updateData: Partial<Omit<AttackData, "id" | "created_at">>,
        trx?: any
    ) {
        const result = await Attack.updateAttack(id, updateData, trx);
        if (!result || result.length === 0) {
            throw new Error("Attack not found");
        }
        return result[0];
    }

    static async findAllAttacks(trx: Knex) {
        return Attack.query(trx).orderBy("created_at", "desc");
    }

    static async findById(id: string, trx: Knex) {
        return Attack.findById(id, trx);
    }
}
