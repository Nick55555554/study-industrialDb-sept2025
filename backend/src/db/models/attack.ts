import { Model } from "./base-model";
import { Rate } from "../../types/rate";
import { TypesOfAttack } from "../../types/type-of-attack";

export interface AttackData {
    id: string;
    name: string;
    frequency: Rate;
    danger: Rate;
    attack_type: TypesOfAttack; // ✅ Consistent naming
    created_at?: Date;
    updated_at?: Date;
}

export class Attack extends Model implements AttackData {
    static readonly tableName = "attacks";
    static readonly idColumn = "id";

    static async createAttack(
        name: string,
        frequency: Rate,
        danger: Rate,
        attack_type: TypesOfAttack,
        trx?: any
    ) {
        return this.query(trx)
            .insert({
                name,
                frequency,
                danger,
                attack_type,
            })
            .returning("*");
    }

    static async findByFrequency(frequency: Rate, trx?: any) {
        return this.query(trx).where("frequency", frequency);
    }

    static async findByDanger(danger: Rate, trx?: any) {
        return this.query(trx).where("danger", danger);
    }

    static async findById(id: string, trx?: any) {
        return this.query(trx).where("id", id).first();
    }

    static async updateAttack(
        id: string,
        updateData: Partial<Omit<AttackData, "id" | "created_at">>,
        trx?: any
    ) {
        return this.query(trx)
            .where({ id })
            .update({
                ...updateData,
                updated_at: new Date(),
            })
            .returning("*");
    }

    id!: string;
    name!: string;
    frequency!: Rate;
    danger!: Rate;
    attack_type!: TypesOfAttack;
    created_at!: Date;
    updated_at!: Date;
}
