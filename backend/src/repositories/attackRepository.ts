import { db } from "../db";
import {
    Attack,
    CreateAttackRequest,
    UpdateAttackRequest,
    AttackFrequency,
    AttackDanger,
    AttackType,
    Target,
    UpdateTargetRequest,
    AttackWithTargets,
    AttackFilter,
    AttackStats,
    Protocol
} from "../models";

export class AttackRepository {
    async create(
        attackData: Omit<Attack, "id" | "created_at" | "updated_at">,
    ): Promise<Attack> {
        const [attack] = await db("ddos_attacks")
            .insert({
                ...attackData,
                source_ips: attackData.source_ips || [],
                affected_ports: attackData.affected_ports || [],
                mitigation_strategies: attackData.mitigation_strategies || [],
                created_at: new Date(),
                updated_at: new Date(),
            })
            .returning("*");

        return attack;
    }

    async findAll(): Promise<Attack[]> {
        return await db("ddos_attacks").select("*");
    }

    async findById(id: string): Promise<Attack | undefined> {
        return await db("ddos_attacks").where({ id }).first();
    }

    async update(
        id: string,
        attackData: UpdateAttackRequest,
    ): Promise<Attack | null> {
        try {
            const updateData: any = {
                ...attackData,
                updated_at: new Date(),
            };

            const [updatedAttack] = await db("ddos_attacks")
                .where({ id })
                .update(updateData)
                .returning("*");

            return updatedAttack || null;
        } catch (error) {
            console.error("Error updating attack:", error);
            return null;
        }
    }

    async updateWithTargets(
        attackId: string,
        attackData: UpdateAttackRequest,
        targetsData?: UpdateTargetRequest[],
    ): Promise<AttackWithTargets | null> {
        return await db.transaction(async (trx) => {
            try {
                // Обновляем атаку
                const [updatedAttack] = await trx("ddos_attacks")
                    .where({ id: attackId })
                    .update({
                        ...attackData,
                        updated_at: new Date(),
                    })
                    .returning("*");

                if (!updatedAttack) {
                    throw new Error("Attack not found");
                }

                // Если переданы цели, обновляем их
                let updatedTargets = [];
                if (targetsData && targetsData.length > 0) {
                    updatedTargets = await this.updateTargetsForAttack(
                        trx,
                        attackId,
                        targetsData,
                    );
                } else {
                    // Получаем текущие цели
                    updatedTargets = await trx("targets").where({
                        attack_id: attackId,
                    });
                }

                return {
                    ...updatedAttack,
                    targets: updatedTargets,
                };
            } catch (error) {
                console.error("Error updating attack with targets:", error);
                throw error;
            }
        });
    }

    private async updateTargetsForAttack(
        trx: any,
        attackId: string,
        targetsData: UpdateTargetRequest[],
    ): Promise<Target[]> {
        // Удаляем старые цели и создаем новые
        await trx("targets").where({ attack_id: attackId }).delete();

        if (targetsData.length === 0) {
            return [];
        }

        const targetsToCreate = targetsData.map((target) => ({
            attack_id: attackId,
            target_ip: target.target_ip!,
            target_domain: target.target_domain || null,
            port: target.port || null,
            protocol: target.protocol || null,
            tags: target.tags || [],
            created_at: new Date(),
        }));

        const createdTargets = await trx("targets")
            .insert(targetsToCreate)
            .returning("*");

        return createdTargets;
    }

    async delete(id: string): Promise<boolean> {
        const result = await db("ddos_attacks").where({ id }).delete();
        return result > 0;
    }

    async createTables(): Promise<void> {
        const attacksTableExists = await db.schema.hasTable("ddos_attacks");
        const targetsTableExists = await db.schema.hasTable("targets");

        if (attacksTableExists && targetsTableExists) {
            console.log("Tables already exist");
            return;
        }

        await db.transaction(async (trx) => {
            if (!attacksTableExists) {
                await trx.schema.createTable("ddos_attacks", (table) => {
                    table
                        .uuid("id")
                        .primary()
                        .defaultTo(db.raw("gen_random_uuid()"));
                    table.string("name").notNullable();

                    // ENUM поля
                    table
                        .enu("frequency", [
                            AttackFrequency.LOW,
                            AttackFrequency.MEDIUM,
                            AttackFrequency.HIGH,
                            AttackFrequency.VERY_HIGH,
                        ])
                        .notNullable();

                    table
                        .enu("danger", [
                            AttackDanger.LOW,
                            AttackDanger.MEDIUM,
                            AttackDanger.HIGH,
                            AttackDanger.CRITICAL,
                        ])
                        .notNullable();

                    table
                        .enu("attack_type", [
                            AttackType.VOLUMETRIC,
                            AttackType.PROTOCOL,
                            AttackType.APPLICATION,
                            AttackType.AMPLIFICATION,
                        ])
                        .notNullable();

                    // Нативные массивы PostgreSQL
                    table.specificType("source_ips", "text[]").defaultTo("{}");
                    table
                        .specificType("affected_ports", "integer[]")
                        .defaultTo("{}");
                    table
                        .specificType("mitigation_strategies", "text[]")
                        .defaultTo("{}");

                    table.timestamp("created_at").defaultTo(db.fn.now());
                    table.timestamp("updated_at").defaultTo(db.fn.now());
                });
                console.log("Table ddos_attacks created");
            }

            if (!targetsTableExists) {
                await trx.schema.createTable("targets", (table) => {
                    table
                        .uuid("id")
                        .primary()
                        .defaultTo(db.raw("gen_random_uuid()"));
                    table.uuid("attack_id").notNullable();
                    table.string("target_ip");
                    table.string("target_domain");
                    table.integer("port");

                    // ENUM для протокола
                    table.enu("protocol", [
                        "http",
                        "https",
                        "tcp",
                        "udp",
                        "ssh",
                        "dns",
                    ]);

                    // Нативный массив тегов
                    table.specificType("tags", "text[]").defaultTo("{}");
                    table.timestamp("created_at").defaultTo(db.fn.now());

                    table
                        .foreign("attack_id")
                        .references("id")
                        .inTable("ddos_attacks")
                        .onDelete("CASCADE");
                });
                console.log("Table targets created");
            }
        });
    }

    async dropTables(): Promise<void> {
        await db.transaction(async (trx) => {
            await trx.schema.dropTableIfExists("targets");
            await trx.schema.dropTableIfExists("ddos_attacks");
        });
        console.log("Tables dropped");
    }

    async checkTablesExist(): Promise<boolean> {
        try {
            const attacksExists = await db.schema.hasTable("ddos_attacks");
            const targetsExists = await db.schema.hasTable("targets");
            return attacksExists && targetsExists;
        } catch (error) {
            return false;
        }
    }

    async findByFilters(filters: AttackFilter): Promise<Attack[]> {
        let query = db('ddos_attacks')
            .select('ddos_attacks.*')
            .distinct('ddos_attacks.id');

        // Фильтр по frequency
        if (filters.frequency) {
            if (Array.isArray(filters.frequency)) {
                query = query.whereIn('ddos_attacks.frequency', filters.frequency);
            } else {
                query = query.where('ddos_attacks.frequency', filters.frequency);
            }
        }

        // Фильтр по danger
        if (filters.danger) {
            if (Array.isArray(filters.danger)) {
                query = query.whereIn('ddos_attacks.danger', filters.danger);
            } else {
                query = query.where('ddos_attacks.danger', filters.danger);
            }
        }

        // Фильтр по attack_type
        if (filters.attack_type) {
            if (Array.isArray(filters.attack_type)) {
                query = query.whereIn('ddos_attacks.attack_type', filters.attack_type);
            } else {
                query = query.where('ddos_attacks.attack_type', filters.attack_type);
            }
        }

        // Фильтр по protocol (из таблицы targets)
        if (filters.protocol) {
            query = query
                .leftJoin('targets', 'ddos_attacks.id', 'targets.attack_id');

            if (Array.isArray(filters.protocol)) {
                query = query.whereIn('targets.protocol', filters.protocol);
            } else {
                query = query.where('targets.protocol', filters.protocol);
            }
        }

        // Фильтр по дате
        if (filters.date_from) {
            query = query.where('ddos_attacks.created_at', '>=', filters.date_from);
        }

        if (filters.date_to) {
            query = query.where('ddos_attacks.created_at', '<=', filters.date_to);
        }

        // Поиск по имени
        if (filters.search) {
            query = query.where('ddos_attacks.name', 'ilike', `%${filters.search}%`);
        }

        const attacks = await query;
        return attacks;
    }

    async getStats(): Promise<AttackStats> {
        // Общее количество атак
        const totalResult = await db('ddos_attacks').count('id as count').first();
        const total = parseInt(totalResult?.count as string) || 0;

        // Статистика по frequency
        const frequencyStats = await db('ddos_attacks')
            .select('frequency')
            .count('id as count')
            .groupBy('frequency');

        const byFrequency = this.initializeEnumObject(AttackFrequency);
        frequencyStats.forEach(stat => {
            byFrequency[stat.frequency as AttackFrequency] = parseInt(stat.count as string);
        });

        // Статистика по danger
        const dangerStats = await db('ddos_attacks')
            .select('danger')
            .count('id as count')
            .groupBy('danger');

        const byDanger = this.initializeEnumObject(AttackDanger);
        dangerStats.forEach(stat => {
            byDanger[stat.danger as AttackDanger] = parseInt(stat.count as string);
        });

        // Статистика по attack_type
        const typeStats = await db('ddos_attacks')
            .select('attack_type')
            .count('id as count')
            .groupBy('attack_type');

        const byType = this.initializeEnumObject(AttackType);
        typeStats.forEach(stat => {
            byType[stat.attack_type as AttackType] = parseInt(stat.count as string);
        });

        // Количество атак за последние 7 дней
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);

        const recentResult = await db('ddos_attacks')
            .where('created_at', '>=', weekAgo)
            .count('id as count')
            .first();

        const recent = parseInt(recentResult?.count as string) || 0;

        return {
            total,
            byFrequency,
            byDanger,
            byType,
            recent
        };
    }

    async getAvailableFilters(): Promise<{
        frequencies: AttackFrequency[];
        dangers: AttackDanger[];
        attackTypes: AttackType[];
        protocols: Protocol[];
    }> {
        // Получаем уникальные значения из базы данных
        const frequencies = await db('ddos_attacks')
            .distinct('frequency')
            .pluck('frequency');

        const dangers = await db('ddos_attacks')
            .distinct('danger')
            .pluck('danger');

        const attackTypes = await db('ddos_attacks')
            .distinct('attack_type')
            .pluck('attack_type');

        const protocols = await db('targets')
            .distinct('protocol')
            .whereNotNull('protocol')
            .pluck('protocol');

        return {
            frequencies: frequencies as AttackFrequency[],
            dangers: dangers as AttackDanger[],
            attackTypes: attackTypes as AttackType[],
            protocols: protocols as Protocol[]
        };
    }

   private initializeEnumObject<T extends string>(enumObj: any): Record<T, number> {
    const result = {} as Record<T, number>;

    // Более безопасный подход - используем Object.keys и фильтруем числовые ключи
    Object.keys(enumObj)
        .filter(key => isNaN(Number(key))) // Игнорируем числовые ключи (reverse mapping)
        .forEach(key => {
            result[enumObj[key] as T] = 0;
        });

    return result;
}
}