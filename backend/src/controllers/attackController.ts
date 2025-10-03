import { Request, Response } from 'express';
import { AttackService } from '../services/attackService';
import { appLogger, errorLogger } from '../logger';

const attackService = new AttackService();

export class AttackController {
    async createAttack(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            appLogger.info('Creating attack request', {
                requestId,
                body: req.body
            });

            const attack = await attackService.createAttackWithTargets(req.body);

            appLogger.info('Attack created successfully', {
                requestId,
                attackId: attack.id
            });

            res.status(201).json({
                success: true,
                message: "Attack created successfully",
                data: attack
            });
        } catch (error: any) {
            errorLogger.error('Error in createAttack controller', {
                requestId,
                error: error.message,
                stack: error.stack,
                body: req.body
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAttack(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { id } = req.params;

            appLogger.info('Getting attack request', {
                requestId,
                attackId: id
            });

            const attack = await attackService.getAttackWithTargets(id);

            if (!attack) {
                appLogger.warn('Attack not found', {
                    requestId,
                    attackId: id
                });

                return res.status(404).json({
                    success: false,
                    message: "Attack not found"
                });
            }

            appLogger.info('Attack retrieved successfully', {
                requestId,
                attackId: id
            });

            res.json({
                success: true,
                data: attack
            });
        } catch (error: any) {
            errorLogger.error('Error in getAttack controller', {
                requestId,
                attackId: req.params.id,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async getAllAttacks(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            appLogger.info('Getting all attacks request', { requestId });

            const attacks = await attackService.getAllAttacks();

            appLogger.info('All attacks retrieved successfully', {
                requestId,
                count: attacks.length
            });

            res.json({
                success: true,
                data: attacks
            });
        } catch (error: any) {
            errorLogger.error('Error in getAllAttacks controller', {
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

    async updateAttack(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { id } = req.params;
            const attackData = req.body;

            appLogger.info('Updating attack request', {
                requestId,
                attackId: id,
                updates: attackData
            });

            const updatedAttack = await attackService.updateAttack(id, attackData);

            if (!updatedAttack) {
                appLogger.warn('Attack not found for update', {
                    requestId,
                    attackId: id
                });

                return res.status(404).json({
                    success: false,
                    message: "Attack not found"
                });
            }

            appLogger.info('Attack updated successfully', {
                requestId,
                attackId: id
            });

            res.json({
                success: true,
                message: "Attack updated successfully",
                data: updatedAttack
            });
        } catch (error: any) {
            errorLogger.error('Error in updateAttack controller', {
                requestId,
                attackId: req.params.id,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async updateAttackWithTargets(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { id } = req.params;
            const { attack, targets } = req.body;

            appLogger.info('Updating attack with targets request', {
                requestId,
                attackId: id,
                targetsCount: targets?.length || 0
            });

            const updatedAttack = await attackService.updateAttackWithTargets(id, attack, targets);

            if (!updatedAttack) {
                appLogger.warn('Attack not found for update with targets', {
                    requestId,
                    attackId: id
                });

                return res.status(404).json({
                    success: false,
                    message: "Attack not found"
                });
            }

            appLogger.info('Attack with targets updated successfully', {
                requestId,
                attackId: id,
                targetsCount: updatedAttack.targets.length
            });

            res.json({
                success: true,
                message: "Attack with targets updated successfully",
                data: updatedAttack
            });
        } catch (error: any) {
            errorLogger.error('Error in updateAttackWithTargets controller', {
                requestId,
                attackId: req.params.id,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async updateAttackTargets(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { id } = req.params;
            const { targets } = req.body;

            appLogger.info('Updating attack targets request', {
                requestId,
                attackId: id,
                targetsCount: targets?.length || 0
            });

            const updatedTargets = await attackService.updateAttackTargets(id, targets);

            appLogger.info('Attack targets updated successfully', {
                requestId,
                attackId: id,
                targetsCount: updatedTargets.length
            });

            res.json({
                success: true,
                message: "Attack targets updated successfully",
                data: updatedTargets
            });
        } catch (error: any) {
            errorLogger.error('Error in updateAttackTargets controller', {
                requestId,
                attackId: req.params.id,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async updateTarget(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { id } = req.params;
            const targetData = req.body;

            appLogger.info('Updating target request', {
                requestId,
                targetId: id,
                updates: targetData
            });

            const updatedTarget = await attackService.updateTarget(id, targetData);

            if (!updatedTarget) {
                appLogger.warn('Target not found for update', {
                    requestId,
                    targetId: id
                });

                return res.status(404).json({
                    success: false,
                    message: "Target not found"
                });
            }

            appLogger.info('Target updated successfully', {
                requestId,
                targetId: id
            });

            res.json({
                success: true,
                message: "Target updated successfully",
                data: updatedTarget
            });
        } catch (error: any) {
            errorLogger.error('Error in updateTarget controller', {
                requestId,
                targetId: req.params.id,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async deleteAttack(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            const { id } = req.params;

            appLogger.info('Deleting attack request', {
                requestId,
                attackId: id
            });

            const deleted = await attackService.deleteAttack(id);

            if (!deleted) {
                appLogger.warn('Attack not found for deletion', {
                    requestId,
                    attackId: id
                });

                return res.status(404).json({
                    success: false,
                    message: "Attack not found"
                });
            }

            appLogger.info('Attack deleted successfully', {
                requestId,
                attackId: id
            });

            res.json({
                success: true,
                message: "Attack deleted successfully"
            });
        } catch (error: any) {
            errorLogger.error('Error in deleteAttack controller', {
                requestId,
                attackId: req.params.id,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    async initializeDatabase(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            appLogger.info('Initializing database request', { requestId });

            const result = await attackService.initializeDatabase();

            if (result.success) {
                appLogger.info('Database initialized successfully', { requestId });
                res.status(201).json({
                    success: true,
                    message: result.message
                });
            } else {
                appLogger.info('Database already initialized', { requestId });
                res.status(409).json({
                    success: false,
                    message: result.message
                });
            }
        } catch (error: any) {
            errorLogger.error('Error in initializeDatabase controller', {
                requestId,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: 'Failed to initialize database'
            });
        }
    }

    async resetDatabase(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            appLogger.info('Resetting database request', { requestId });

            if (process.env.NODE_ENV === 'production') {
                appLogger.warn('Database reset attempted in production', { requestId });
                return res.status(403).json({
                    success: false,
                    message: 'Database reset is not allowed in production'
                });
            }

            const result = await attackService.resetDatabase();

            appLogger.info('Database reset successfully', { requestId });

            res.json({
                success: result.success,
                message: result.message
            });
        } catch (error: any) {
            errorLogger.error('Error in resetDatabase controller', {
                requestId,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: 'Failed to reset database'
            });
        }
    }

    async getDatabaseStatus(req: Request, res: Response) {
        const requestId = Math.random().toString(36).substring(7);

        try {
            appLogger.info('Getting database status request', { requestId });

            const status = await attackService.getDatabaseStatus();

            appLogger.info('Database status retrieved successfully', { requestId });

            res.json({
                success: true,
                data: status
            });
        } catch (error: any) {
            errorLogger.error('Error in getDatabaseStatus controller', {
                requestId,
                error: error.message,
                stack: error.stack
            });

            res.status(500).json({
                success: false,
                message: 'Failed to get database status'
            });
        }
    }
}