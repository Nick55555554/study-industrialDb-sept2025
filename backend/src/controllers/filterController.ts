import { Request, Response } from 'express';
import { AttackService } from '../services/attackService';
import { AttackFilter, AttackFrequency, AttackDanger, AttackType, Protocol } from '../models';

const attackService = new AttackService();

export class FilterController {
    async getAttacksByFilters(req: Request, res: Response) {
        try {
            const filters: AttackFilter = req.query;

            // Валидация enum значений
            if (filters.frequency) {
                const validFrequencies = Object.values(AttackFrequency);
                if (Array.isArray(filters.frequency)) {
                    const invalid = filters.frequency.filter(f => !validFrequencies.includes(f));
                    if (invalid.length > 0) {
                        return res.status(400).json({
                            success: false,
                            message: `Invalid frequency values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validFrequencies.includes(filters.frequency)) {
                    return res.status(400).json({
                        success: false,
                        message: `Invalid frequency value: ${filters.frequency}`
                    });
                }
            }

            if (filters.danger) {
                const validDangers = Object.values(AttackDanger);
                if (Array.isArray(filters.danger)) {
                    const invalid = filters.danger.filter(d => !validDangers.includes(d));
                    if (invalid.length > 0) {
                        return res.status(400).json({
                            success: false,
                            message: `Invalid danger values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validDangers.includes(filters.danger)) {
                    return res.status(400).json({
                        success: false,
                        message: `Invalid danger value: ${filters.danger}`
                    });
                }
            }

            if (filters.attack_type) {
                const validTypes = Object.values(AttackType);
                if (Array.isArray(filters.attack_type)) {
                    const invalid = filters.attack_type.filter(t => !validTypes.includes(t));
                    if (invalid.length > 0) {
                        return res.status(400).json({
                            success: false,
                            message: `Invalid attack type values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validTypes.includes(filters.attack_type)) {
                    return res.status(400).json({
                        success: false,
                        message: `Invalid attack type value: ${filters.attack_type}`
                    });
                }
            }

            if (filters.protocol) {
                const validProtocols = Object.values(Protocol);
                if (Array.isArray(filters.protocol)) {
                    const invalid = filters.protocol.filter(p => !validProtocols.includes(p));
                    if (invalid.length > 0) {
                        return res.status(400).json({
                            success: false,
                            message: `Invalid protocol values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validProtocols.includes(filters.protocol)) {
                    return res.status(400).json({
                        success: false,
                        message: `Invalid protocol value: ${filters.protocol}`
                    });
                }
            }

            const attacks = await attackService.getAttacksByFilters(filters);

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                filters
            });
        } catch (error: any) {
            console.error("Get attacks by filters error:", error);
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttackStats(req: Request, res: Response) {
        try {
            const stats = await attackService.getAttackStats();

            res.json({
                success: true,
                data: stats
            });
        } catch (error: any) {
            console.error("Get attack stats error:", error);
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAvailableFilters(req: Request, res: Response) {
        try {
            const filters = await attackService.getAvailableFilters();

            res.json({
                success: true,
                data: filters
            });
        } catch (error: any) {
            console.error("Get available filters error:", error);
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByFrequency(req: Request, res: Response) {
        try {
            const { frequency } = req.params;

            if (!Object.values(AttackFrequency).includes(frequency as AttackFrequency)) {
                return res.status(400).json({
                    success: false,
                    message: `Invalid frequency. Available values: ${Object.values(AttackFrequency).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByFrequency(frequency as AttackFrequency);

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                frequency
            });
        } catch (error: any) {
            console.error("Get attacks by frequency error:", error);
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByDanger(req: Request, res: Response) {
        try {
            const { danger } = req.params;

            if (!Object.values(AttackDanger).includes(danger as AttackDanger)) {
                return res.status(400).json({
                    success: false,
                    message: `Invalid danger. Available values: ${Object.values(AttackDanger).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByDanger(danger as AttackDanger);

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                danger
            });
        } catch (error: any) {
            console.error("Get attacks by danger error:", error);
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByType(req: Request, res: Response) {
        try {
            const { type } = req.params;

            if (!Object.values(AttackType).includes(type as AttackType)) {
                return res.status(400).json({
                    success: false,
                    message: `Invalid attack type. Available values: ${Object.values(AttackType).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByType(type as AttackType);

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                attack_type: type
            });
        } catch (error: any) {
            console.error("Get attacks by type error:", error);
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByProtocol(req: Request, res: Response) {
        try {
            const { protocol } = req.params;

            if (!Object.values(Protocol).includes(protocol as Protocol)) {
                return res.status(400).json({
                    success: false,
                    message: `Invalid protocol. Available values: ${Object.values(Protocol).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByProtocol(protocol as Protocol);

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                protocol
            });
        } catch (error: any) {
            console.error("Get attacks by protocol error:", error);
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }
}