import { Request, Response } from 'express';
import { AttackService } from '../services/attackService';
import { AttackFilter, AttackFrequency, AttackDanger, AttackType, Protocol } from '../models';
import { appLogger, errorLogger } from '../logger';

const attackService = new AttackService();

export class FilterController {
    async getAttacksByFilters(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const filters: AttackFilter = req.query;

            appLogger.info('Filtering attacks request', {
                requestId,
                filters
            });

            // Валидация enum значений
            if (filters.frequency) {
                const validFrequencies = Object.values(AttackFrequency);
                if (Array.isArray(filters.frequency)) {
                    const invalid = filters.frequency.filter(f => !validFrequencies.includes(f));
                    if (invalid.length > 0) {
                        appLogger.warn('Invalid frequency values in filter', {
                            requestId,
                            invalidValues: invalid
                        });

                        return res.status(400).json({
                            success: false,
                            message: `Invalid frequency values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validFrequencies.includes(filters.frequency)) {
                    appLogger.warn('Invalid frequency value in filter', {
                        requestId,
                        invalidValue: filters.frequency
                    });

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
                        appLogger.warn('Invalid danger values in filter', {
                            requestId,
                            invalidValues: invalid
                        });

                        return res.status(400).json({
                            success: false,
                            message: `Invalid danger values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validDangers.includes(filters.danger)) {
                    appLogger.warn('Invalid danger value in filter', {
                        requestId,
                        invalidValue: filters.danger
                    });

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
                        appLogger.warn('Invalid attack type values in filter', {
                            requestId,
                            invalidValues: invalid
                        });

                        return res.status(400).json({
                            success: false,
                            message: `Invalid attack type values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validTypes.includes(filters.attack_type)) {
                    appLogger.warn('Invalid attack type value in filter', {
                        requestId,
                        invalidValue: filters.attack_type
                    });

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
                        appLogger.warn('Invalid protocol values in filter', {
                            requestId,
                            invalidValues: invalid
                        });

                        return res.status(400).json({
                            success: false,
                            message: `Invalid protocol values: ${invalid.join(', ')}`
                        });
                    }
                } else if (!validProtocols.includes(filters.protocol)) {
                    appLogger.warn('Invalid protocol value in filter', {
                        requestId,
                        invalidValue: filters.protocol
                    });

                    return res.status(400).json({
                        success: false,
                        message: `Invalid protocol value: ${filters.protocol}`
                    });
                }
            }

            const attacks = await attackService.getAttacksByFilters(filters);

            appLogger.info('Filters applied successfully', {
                requestId,
                filters,
                resultsCount: attacks.length
            });

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                filters
            });
        } catch (error: any) {
            errorLogger.error('Error in getAttacksByFilters controller', {
                requestId,
                filters: req.query,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttackStats(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            appLogger.info('Getting attack statistics request', { requestId });

            const stats = await attackService.getAttackStats();

            appLogger.info('Attack statistics retrieved successfully', { requestId });

            res.json({
                success: true,
                data: stats
            });
        } catch (error: any) {
            errorLogger.error('Error in getAttackStats controller', {
                requestId,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAvailableFilters(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            appLogger.info('Getting available filters request', { requestId });

            const filters = await attackService.getAvailableFilters();

            appLogger.info('Available filters retrieved successfully', { requestId });

            res.json({
                success: true,
                data: filters
            });
        } catch (error: any) {
            errorLogger.error('Error in getAvailableFilters controller', {
                requestId,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByFrequency(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { frequency } = req.params;

            appLogger.info('Getting attacks by frequency request', {
                requestId,
                frequency
            });

            if (!Object.values(AttackFrequency).includes(frequency as AttackFrequency)) {
                appLogger.warn('Invalid frequency value', {
                    requestId,
                    frequency
                });

                return res.status(400).json({
                    success: false,
                    message: `Invalid frequency. Available values: ${Object.values(AttackFrequency).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByFrequency(frequency as AttackFrequency);

            appLogger.info('Attacks by frequency retrieved successfully', {
                requestId,
                frequency,
                count: attacks.length
            });

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                frequency
            });
        } catch (error: any) {
            errorLogger.error('Error in getAttacksByFrequency controller', {
                requestId,
                frequency: req.params.frequency,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByDanger(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { danger } = req.params;

            appLogger.info('Getting attacks by danger request', {
                requestId,
                danger
            });

            if (!Object.values(AttackDanger).includes(danger as AttackDanger)) {
                appLogger.warn('Invalid danger value', {
                    requestId,
                    danger
                });

                return res.status(400).json({
                    success: false,
                    message: `Invalid danger. Available values: ${Object.values(AttackDanger).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByDanger(danger as AttackDanger);

            appLogger.info('Attacks by danger retrieved successfully', {
                requestId,
                danger,
                count: attacks.length
            });

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                danger
            });
        } catch (error: any) {
            errorLogger.error('Error in getAttacksByDanger controller', {
                requestId,
                danger: req.params.danger,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByType(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { type } = req.params;

            appLogger.info('Getting attacks by type request', {
                requestId,
                type
            });

            if (!Object.values(AttackType).includes(type as AttackType)) {
                appLogger.warn('Invalid attack type value', {
                    requestId,
                    type
                });

                return res.status(400).json({
                    success: false,
                    message: `Invalid attack type. Available values: ${Object.values(AttackType).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByType(type as AttackType);

            appLogger.info('Attacks by type retrieved successfully', {
                requestId,
                type,
                count: attacks.length
            });

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                attack_type: type
            });
        } catch (error: any) {
            errorLogger.error('Error in getAttacksByType controller', {
                requestId,
                type: req.params.type,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttacksByProtocol(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { protocol } = req.params;

            appLogger.info('Getting attacks by protocol request', {
                requestId,
                protocol
            });

            if (!Object.values(Protocol).includes(protocol as Protocol)) {
                appLogger.warn('Invalid protocol value', {
                    requestId,
                    protocol
                });

                return res.status(400).json({
                    success: false,
                    message: `Invalid protocol. Available values: ${Object.values(Protocol).join(', ')}`
                });
            }

            const attacks = await attackService.getAttacksByProtocol(protocol as Protocol);

            appLogger.info('Attacks by protocol retrieved successfully', {
                requestId,
                protocol,
                count: attacks.length
            });

            res.json({
                success: true,
                data: attacks,
                count: attacks.length,
                protocol
            });
        } catch (error: any) {
            errorLogger.error('Error in getAttacksByProtocol controller', {
                requestId,
                protocol: req.params.protocol,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }
}