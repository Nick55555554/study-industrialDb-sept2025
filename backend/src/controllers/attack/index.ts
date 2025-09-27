import { AttackData } from "../../db/models/attack";
import e, { Request, Response } from "express";
import { AttackRepository } from "../../repositories/attack-repository";
import db from "../../db";
type CreateAttackBody = Omit<AttackData, "id">;

export const createTableController = async (_req: Request, res: Response) => {
    try {
        await db.schema.createTable("attacks", (table) => {
            table.uuid("id").primary().defaultTo(db.raw("gen_random_uuid()"));
            table.string("name").notNullable();
            table.string("frequency").notNullable();
            table.string("danger").notNullable();
            table.string("attack_type").notNullable();
            table.timestamp("created_at").defaultTo(db.fn.now());
            table.timestamp("updated_at").defaultTo(db.fn.now());
        });

        res.status(200).json({
            success: true,
            message: "Table created successfully",
        });
    } catch (error) {
        console.error("Table creation error:", error);
        res.status(500).json({
            success: false,
            message: "Failed to create table",
        });
    }
};

export const createAttackController = async (
    req: Request<CreateAttackBody>,
    res: Response
) => {
    try {
        const attackData = req.body;

        // Валидация
        if (
            !attackData.name ||
            !attackData.frequency ||
            !attackData.danger ||
            !attackData.attack_type
        ) {
            return res.status(400).json({
                error: "Missing required fields: name, frequency, danger, attack_type",
            });
        }

        await AttackRepository.create(attackData, db);
        return res.status(201).json({
            success: true,
            message: "Attack created successfully",
        });
    } catch (error) {
        console.error("Create attack error:", error);
        return res.status(500).json({
            error: "Internal server error",
        });
    }
};

export const deleteAttackController = async (req: Request, res: Response) => {
    try {
        const { id } = req.body;

        if (!id) {
            return res.status(400).json({ error: "Attack ID is required" });
        }

        await AttackRepository.delById(id, db);
        return res.status(204).send();
    } catch (error) {
        console.error("Delete attack error:", error);
        return res.status(500).json({ error: "Failed to delete attack" });
    }
};

export const updateAttackController = async (req: Request, res: Response) => {
    try {
        const { id, ...updateData } = req.body;

        if (!id) {
            return res.status(400).json({ error: "Attack ID is required" });
        }

        const result = await AttackRepository.update(id, updateData, db);

        if (!result) {
            return res.status(404).json({ error: "Attack not found" });
        }

        return res.status(200).json({
            success: true,
            message: "Attack updated successfully",
        });
    } catch (error) {
        console.error("Update attack error:", error);
        return res.status(500).json({ error: "Failed to update attack" });
    }
};

export const readAllAttacksController = async (
    _req: Request,
    res: Response
) => {
    try {
        const allAttacks = await AttackRepository.findAllAttacks(db);
        return res.status(200).json({
            success: true,
            data: allAttacks,
        });
    } catch (error) {
        console.error("Get attacks error:", error);
        return res.status(500).json({ error: "Failed to fetch attacks" });
    }
};
