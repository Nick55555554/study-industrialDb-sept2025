import { Request, Response } from "express";
import { AttackService } from "../services/attackService";

const attackService = new AttackService();

export class AttackController {
    async initializeDatabase(req: Request, res: Response) {
        try {
            const result = await attackService.initializeDatabase();

            if (result.success) {
                res.status(201).json({
                    success: true,
                    message: result.message,
                });
            } else {
                res.status(409).json({
                    success: false,
                    message: result.message,
                });
            }
        } catch (error) {
            console.error("Initialize database error:", error);
            res.status(500).json({
                success: false,
                message: "Failed to initialize database",
            });
        }
    }

    async resetDatabase(req: Request, res: Response) {
        try {
            if (process.env.NODE_ENV === "production") {
                return res.status(403).json({
                    success: false,
                    message: "Database reset is not allowed in production",
                });
            }

            const result = await attackService.resetDatabase();

            res.json({
                success: result.success,
                message: result.message,
            });
        } catch (error) {
            console.error("Reset database error:", error);
            res.status(500).json({
                success: false,
                message: "Failed to reset database",
            });
        }
    }

    async getDatabaseStatus(req: Request, res: Response) {
        try {
            const status = await attackService.getDatabaseStatus();

            res.json({
                success: true,
                data: status,
            });
        } catch (error) {
            console.error("Get database status error:", error);
            res.status(500).json({
                success: false,
                message: "Failed to get database status",
            });
        }
    }

    async createAttack(req: Request, res: Response) {
        try {
            const attack = await attackService.createAttackWithTargets(
                req.body,
            );

            res.status(201).json({
                success: true,
                message: "Attack created successfully",
                data: attack,
            });
        } catch (error) {
            console.error("Create attack error:", error);
            res.status(500).json({
                success: false,
                message: "Failed to create attack",
            });
        }
    }

    async getAttack(req: Request, res: Response) {
        try {
            const { id } = req.params;
            const attack = await attackService.getAttackWithTargets(id);

            if (!attack) {
                return res.status(404).json({
                    success: false,
                    message: "Attack not found",
                });
            }

            res.json({
                success: true,
                data: attack,
            });
        } catch (error) {
            console.error("Get attack error:", error);
            res.status(500).json({
                success: false,
                message: "Failed to get attack",
            });
        }
    }

    async getAllAttacks(req: Request, res: Response) {
        try {
            const attacks = await attackService.getAllAttacks();

            res.json({
                success: true,
                data: attacks,
            });
        } catch (error) {
            console.error("Get all attacks error:", error);
            res.status(500).json({
                success: false,
                message: "Failed to get attacks",
            });
        }
    }

    async deleteAttack(req: Request, res: Response) {
        try {
            const { id } = req.params;
            const deleted = await attackService.deleteAttack(id);

            if (!deleted) {
                return res.status(404).json({
                    success: false,
                    message: "Attack not found",
                });
            }

            res.json({
                success: true,
                message: "Attack deleted successfully",
            });
        } catch (error) {
            console.error("Delete attack error:", error);
            res.status(500).json({
                success: false,
                message: "Failed to delete attack",
            });
        }
    }
    async updateAttack(req: Request, res: Response) {
        try {
            const { id } = req.params;
            const attackData = req.body;

            const updatedAttack = await attackService.updateAttack(
                id,
                attackData,
            );

            if (!updatedAttack) {
                return res.status(404).json({
                    success: false,
                    message: "Attack not found",
                });
            }

            res.json({
                success: true,
                message: "Attack updated successfully",
                data: updatedAttack,
            });
        } catch (error: any) {
            console.error("Update attack error:", error);
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }

    async updateAttackWithTargets(req: Request, res: Response) {
        try {
            const { id } = req.params;
            const { attack, targets } = req.body;

            const updatedAttack = await attackService.updateAttackWithTargets(
                id,
                attack,
                targets,
            );

            if (!updatedAttack) {
                return res.status(404).json({
                    success: false,
                    message: "Attack not found",
                });
            }

            res.json({
                success: true,
                message: "Attack with targets updated successfully",
                data: updatedAttack,
            });
        } catch (error: any) {
            console.error("Update attack with targets error:", error);
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }

    async updateAttackTargets(req: Request, res: Response) {
        try {
            const { id } = req.params;
            const { targets } = req.body;

            const updatedTargets = await attackService.updateAttackTargets(
                id,
                targets,
            );

            res.json({
                success: true,
                message: "Attack targets updated successfully",
                data: updatedTargets,
            });
        } catch (error: any) {
            console.error("Update attack targets error:", error);
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }

    async updateTarget(req: Request, res: Response) {
        try {
            const { id } = req.params;
            const targetData = req.body;

            const updatedTarget = await attackService.updateTarget(
                id,
                targetData,
            );

            if (!updatedTarget) {
                return res.status(404).json({
                    success: false,
                    message: "Target not found",
                });
            }

            res.json({
                success: true,
                message: "Target updated successfully",
                data: updatedTarget,
            });
        } catch (error: any) {
            console.error("Update target error:", error);
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }
}
