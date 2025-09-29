import { db } from '../db/index';
import { Attack, CreateAttackRequest } from '../models';

export class AttackRepository {
    async create(attackData: Omit<Attack, 'id' | 'created_at' | 'updated_at'>): Promise<Attack> {
        const [attack] = await db('ddos_attacks')
            .insert({
                ...attackData,
                created_at: new Date(),
                updated_at: new Date()
            })
            .returning('*');
        return attack;
    }

    async findAll(): Promise<Attack[]> {
        return await db('ddos_attacks').select('*');
    }

    async findById(id: string): Promise<Attack | undefined> {
        return await db('ddos_attacks').where({ id }).first();
    }

    async update(id: string, attackData: Partial<Attack>): Promise<Attack | undefined> {
        const [attack] = await db('ddos_attacks')
            .where({ id })
            .update({
                ...attackData,
                updated_at: new Date()
            })
            .returning('*');
        return attack;
    }

    async delete(id: string): Promise<boolean> {
        const result = await db('ddos_attacks').where({ id }).delete();
        return result > 0;
    }
    async createTables(): Promise<void> {
        await db.transaction(async (trx) => {
            // Создаем таблицу attacks
            await trx.schema.createTable('ddos_attacks', (table) => {
                table.uuid('id').primary().defaultTo(db.raw('gen_random_uuid()'));
                table.string('name').notNullable();
                table.string('frequency').notNullable();
                table.string('danger').notNullable();
                table.string('attack_type').notNullable();
                table.timestamp('created_at').defaultTo(db.fn.now());
                table.timestamp('updated_at').defaultTo(db.fn.now());
            });

            // Создаем таблицу targets
            await trx.schema.createTable('targets', (table) => {
                table.uuid('id').primary().defaultTo(db.raw('gen_random_uuid()'));
                table.uuid('attack_id').notNullable();
                table.string('target_ip').notNullable();
                table.string('target_domain');
                table.integer('port');
                table.string('protocol');
                table.timestamp('created_at').defaultTo(db.fn.now());

                // Внешний ключ
                table.foreign('attack_id')
                     .references('id')
                     .inTable('ddos_attacks')
                     .onDelete('CASCADE');
            });
        });
    }

    async dropTables(): Promise<void> {
        await db.transaction(async (trx) => {
            await trx.schema.dropTableIfExists('targets');
            await trx.schema.dropTableIfExists('ddos_attacks');
        });
    }

    async checkTablesExist(): Promise<boolean> {
        try {
            // Проверяем существование таблиц
            console.log('999999')
            const attacksExists = await db.schema.hasTable('ddos_attacks');
            console.log('9988888888')
            const targetsExists = await db.schema.hasTable('targets');
            console.log(targetsExists, attacksExists, 'dfghjkl')
            return attacksExists && targetsExists;
        } catch (error) {
            return false;
        }
    }
}