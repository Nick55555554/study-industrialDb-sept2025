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
import { dbLogger } from '../logger';

export class AttackRepository {
    async create(
        attackData: Omit<Attack, "id" | "created_at" | "updated_at">,
    ): Promise<Attack> {
        try {
            dbLogger.info('Creating new attack', {
                name: attackData.name,
                attackType: attackData.attack_type
            });

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

            dbLogger.info('Attack created successfully', {
                attackId: attack.id,
                name: attack.name
            });

            return attack;
        } catch (error: any) {
            dbLogger.error('Error creating attack', {
                error: error.message,
                attackData: {
                    name: attackData.name,
                    type: attackData.attack_type
                }
            });
            throw error;
        }
    }

    async findAll(): Promise<Attack[]> {
        try {
            dbLogger.debug('Finding all attacks');
            const attacks = await db("ddos_attacks").select("*");
            dbLogger.debug('Found all attacks', { count: attacks.length });
            return attacks;
        } catch (error: any) {
            dbLogger.error('Error finding all attacks', { error: error.message });
            throw error;
        }
    }

    async findById(id: string): Promise<Attack | undefined> {
        try {
            dbLogger.debug('Finding attack by ID', { attackId: id });
            const attack = await db("ddos_attacks").where({ id }).first();

            if (attack) {
                dbLogger.debug('Attack found by ID', { attackId: id });
            } else {
                dbLogger.debug('Attack not found by ID', { attackId: id });
            }

            return attack;
        } catch (error: any) {
            dbLogger.error('Error finding attack by ID', { attackId: id, error: error.message });
            throw error;
        }
    }

    async update(
        id: string,
        attackData: UpdateAttackRequest,
    ): Promise<Attack | null> {
        try {
            dbLogger.info('Updating attack', { attackId: id, updates: attackData });

            const updateData: any = {
                ...attackData,
                updated_at: new Date(),
            };

            const [updatedAttack] = await db("ddos_attacks")
                .where({ id })
                .update(updateData)
                .returning("*");

            if (updatedAttack) {
                dbLogger.info('Attack updated successfully', { attackId: id });
            } else {
                dbLogger.warn('Attack not found for update', { attackId: id });
            }

            return updatedAttack || null;
        } catch (error: any) {
            dbLogger.error('Error updating attack', {
                attackId: id,
                error: error.message,
                updates: attackData
            });
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
                dbLogger.info('Updating attack with targets', {
                    attackId,
                    targetsCount: targetsData?.length || 0
                });

                const [updatedAttack] = await trx("ddos_attacks")
                    .where({ id: attackId })
                    .update({
                        ...attackData,
                        updated_at: new Date(),
                    })
                    .returning("*");

                if (!updatedAttack) {
                    dbLogger.warn('Attack not found for update with targets', { attackId });
                    throw new Error("Attack not found");
                }

                let updatedTargets = [];
                if (targetsData && targetsData.length > 0) {
                    updatedTargets = await this.updateTargetsForAttack(
                        trx,
                        attackId,
                        targetsData,
                    );
                } else {
                    updatedTargets = await trx("targets").where({
                        attack_id: attackId,
                    });
                }

                dbLogger.info('Attack with targets updated successfully', {
                    attackId,
                    targetsCount: updatedTargets.length
                });

                return {
                    ...updatedAttack,
                    targets: updatedTargets,
                };
            } catch (error: any) {
                dbLogger.error('Error updating attack with targets', {
                    attackId,
                    error: error.message,
                    stack: error.stack
                });
                throw error;
            }
        });
    }

    private async updateTargetsForAttack(
        trx: any,
        attackId: string,
        targetsData: UpdateTargetRequest[],
    ): Promise<Target[]> {
        try {
            dbLogger.debug('Updating targets for attack', { attackId, targetsCount: targetsData.length });

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

            dbLogger.debug('Targets updated successfully', {
                attackId,
                targetsCount: createdTargets.length
            });

            return createdTargets;
        } catch (error: any) {
            dbLogger.error('Error updating targets for attack', {
                attackId,
                error: error.message
            });
            throw error;
        }
    }

    async delete(id: string): Promise<boolean> {
        try {
            dbLogger.info('Deleting attack', { attackId: id });

            const result = await db("ddos_attacks").where({ id }).delete();
            const success = result > 0;

            if (success) {
                dbLogger.info('Attack deleted successfully', { attackId: id });
            } else {
                dbLogger.warn('Attack not found for deletion', { attackId: id });
            }

            return success;
        } catch (error: any) {
            dbLogger.error('Error deleting attack', {
                attackId: id,
                error: error.message
            });
            return false;
        }
    }

    async createTables(): Promise<void> {
        try {
            dbLogger.info('Checking database tables existence');

            const attacksTableExists = await db.schema.hasTable("ddos_attacks");
            const targetsTableExists = await db.schema.hasTable("targets");

            if (attacksTableExists && targetsTableExists) {
                dbLogger.info('Tables already exist');
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

                        table.specificType("source_ips", "text[]").defaultTo("{}");
                        table
                            .specificType("affected_ports", "integer[]")
                            .defaultTo("{}");
                        table
                            .specificType("mitigation_strategies", "text[]")
                            .defaultTo("{}");

                        table.timestamp("created_at").defaultTo(db.fn.now());
                        table.timestamp("updated_at").defaultTo(db.fn.now());

                        table.check('LENGTH(name) >= 3 AND LENGTH(name) <= 40', [], 'ddos_attacks');
                    });
                    dbLogger.info('Table ddos_attacks created');
                }

                if (!targetsTableExists) {
                    await trx.schema.createTable("targets", (table) => {
                        table
                            .uuid("id")
                            .primary()
                            .defaultTo(db.raw("gen_random_uuid()"));
                        table.uuid("attack_id").notNullable();
                        table.string("target_ip").notNullable();
                        table.string("target_domain");
                        table.integer("port");

                        table.enu("protocol", [
                            "http",
                            "https",
                            "tcp",
                            "udp",
                            "ssh",
                            "dns",
                        ]);

                        table.specificType("tags", "text[]").defaultTo("{}");
                        table.timestamp("created_at").defaultTo(db.fn.now());

                        table
                            .foreign("attack_id")
                            .references("id")
                            .inTable("ddos_attacks")
                            .onDelete("CASCADE");
                    });
                    dbLogger.info('Table targets created');
                }
            });

            dbLogger.info('Database tables created successfully');
        } catch (error: any) {
            dbLogger.error('Error creating database tables', {
                error: error.message,
                stack: error.stack
            });
            throw error;
        }
    }

    async dropTables(): Promise<void> {
        try {
            dbLogger.info('Dropping database tables');

            await db.transaction(async (trx) => {
                await trx.schema.dropTableIfExists("targets");
                await trx.schema.dropTableIfExists("ddos_attacks");
            });

            dbLogger.info('Database tables dropped successfully');
        } catch (error: any) {
            dbLogger.error('Error dropping database tables', {
                error: error.message
            });
            throw error;
        }
    }

    async checkTablesExist(): Promise<boolean> {
        try {
            dbLogger.debug('Checking if tables exist');
            const attacksExists = await db.schema.hasTable("ddos_attacks");
            const targetsExists = await db.schema.hasTable("targets");
            const exists = attacksExists && targetsExists;

            dbLogger.debug('Tables existence check result', { exists });
            return exists;
        } catch (error: any) {
            dbLogger.error('Error checking tables existence', { error: error.message });
            return false;
        }
    }

    async findByFilters(filters: AttackFilter): Promise<Attack[]> {
        try {
            dbLogger.debug('Finding attacks by filters', { filters });

            let query = db('ddos_attacks')
                .select('ddos_attacks.*')
                .distinct('ddos_attacks.id');

            if (filters.frequency) {
                if (Array.isArray(filters.frequency)) {
                    query = query.whereIn('ddos_attacks.frequency', filters.frequency);
                } else {
                    query = query.where('ddos_attacks.frequency', filters.frequency);
                }
            }

            if (filters.danger) {
                if (Array.isArray(filters.danger)) {
                    query = query.whereIn('ddos_attacks.danger', filters.danger);
                } else {
                    query = query.where('ddos_attacks.danger', filters.danger);
                }
            }

            if (filters.attack_type) {
                if (Array.isArray(filters.attack_type)) {
                    query = query.whereIn('ddos_attacks.attack_type', filters.attack_type);
                } else {
                    query = query.where('ddos_attacks.attack_type', filters.attack_type);
                }
            }

            if (filters.protocol) {
                query = query
                    .leftJoin('targets', 'ddos_attacks.id', 'targets.attack_id');

                if (Array.isArray(filters.protocol)) {
                    query = query.whereIn('targets.protocol', filters.protocol);
                } else {
                    query = query.where('targets.protocol', filters.protocol);
                }
            }

            if (filters.date_from) {
                query = query.where('ddos_attacks.created_at', '>=', filters.date_from);
            }

            if (filters.date_to) {
                query = query.where('ddos_attacks.created_at', '<=', filters.date_to);
            }

            if (filters.search) {
                query = query.where('ddos_attacks.name', 'ilike', `%${filters.search}%`);
            }

            const attacks = await query;

            dbLogger.debug('Found attacks by filters', {
                filter: filters,
                count: attacks.length
            });

            return attacks;
        } catch (error: any) {
            dbLogger.error('Error finding attacks by filters', {
                filters,
                error: error.message
            });
            throw error;
        }
    }

    async getStats(): Promise<AttackStats> {
        try {
            dbLogger.debug('Getting attack statistics');

            const totalResult = await db('ddos_attacks').count('id as count').first();
            const total = parseInt(totalResult?.count as string) || 0;

            const frequencyStats = await db('ddos_attacks')
                .select('frequency')
                .count('id as count')
                .groupBy('frequency');

            const byFrequency = this.initializeEnumObject(AttackFrequency);
            frequencyStats.forEach(stat => {
                byFrequency[stat.frequency as AttackFrequency] = parseInt(stat.count as string);
            });

            const dangerStats = await db('ddos_attacks')
                .select('danger')
                .count('id as count')
                .groupBy('danger');

            const byDanger = this.initializeEnumObject(AttackDanger);
            dangerStats.forEach(stat => {
                byDanger[stat.danger as AttackDanger] = parseInt(stat.count as string);
            });

            const typeStats = await db('ddos_attacks')
                .select('attack_type')
                .count('id as count')
                .groupBy('attack_type');

            const byType = this.initializeEnumObject(AttackType);
            typeStats.forEach(stat => {
                byType[stat.attack_type as AttackType] = parseInt(stat.count as string);
            });

            const weekAgo = new Date();
            weekAgo.setDate(weekAgo.getDate() - 7);

            const recentResult = await db('ddos_attacks')
                .where('created_at', '>=', weekAgo)
                .count('id as count')
                .first();

            const recent = parseInt(recentResult?.count as string) || 0;

            dbLogger.debug('Attack statistics retrieved', { total, recent });

            return {
                total,
                byFrequency,
                byDanger,
                byType,
                recent
            };
        } catch (error: any) {
            dbLogger.error('Error getting attack statistics', { error: error.message });
            throw error;
        }
    }

    async getAvailableFilters(): Promise<{
        frequencies: AttackFrequency[];
        dangers: AttackDanger[];
        attackTypes: AttackType[];
        protocols: Protocol[];
    }> {
        try {
            dbLogger.debug('Getting available filters');

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

            const filters = {
                frequencies: frequencies as AttackFrequency[],
                dangers: dangers as AttackDanger[],
                attackTypes: attackTypes as AttackType[],
                protocols: protocols as Protocol[]
            };

            dbLogger.debug('Available filters retrieved', filters);

            return filters;
        } catch (error: any) {
            dbLogger.error('Error getting available filters', { error: error.message });
            throw error;
        }
    }

    private initializeEnumObject<T extends string>(enumObj: any): Record<T, number> {
        const result = {} as Record<T, number>;
        Object.values(enumObj).forEach(value => {
            if (typeof value === 'string') {
                result[value as T] = 0;
            }
        });
        return result;
    }
}