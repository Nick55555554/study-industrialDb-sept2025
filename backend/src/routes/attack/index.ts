import { Router } from "express";
import {
    createAttackController,
    createTableController,
    deleteAttackController,
    readAllAttacksController,
    updateAttackController,
} from "../../controllers/attack";

const router = Router();

/**
 * @swagger
 * /attack/init:
 *   post:
 *     summary: Создать таблицу attacks
 *     tags: [Attacks]
 *     responses:
 *       200:
 *         description: Таблица успешно создана
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 message:
 *                   type: string
 *       500:
 *         description: Ошибка при создании таблицы
 */
router.post("/init", createTableController);

/**
 * @swagger
 * /attack:
 *   post:
 *     summary: Создать новую атаку
 *     tags: [Attacks]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - frequency
 *               - danger
 *               - attack_type
 *             properties:
 *               name:
 *                 type: string
 *                 example: "DDoS Attack"
 *               frequency:
 *                 type: string
 *                 example: "High"
 *               danger:
 *                 type: string
 *                 example: "Critical"
 *               attack_type:
 *                 type: string
 *                 example: "Network"
 *     responses:
 *       201:
 *         description: Атака успешно создана
 *       500:
 *         description: Ошибка при создании атаки
 */
router.post("/", createAttackController);

/**
 * @swagger
 * /attack:
 *   get:
 *     summary: Получить все атаки
 *     tags: [Attacks]
 *     responses:
 *       200:
 *         description: Список всех атак
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data:
 *                   type: array
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: string
 *                         format: uuid
 *                       name:
 *                         type: string
 *                       frequency:
 *                         type: string
 *                       danger:
 *                         type: string
 *                       attack_type:
 *                         type: string
 *                       created_at:
 *                         type: string
 *                         format: date-time
 *                       updated_at:
 *                         type: string
 *                         format: date-time
 */
router.get("/", readAllAttacksController);

/**
 * @swagger
 * /attack:
 *   patch:
 *     summary: Обновить атаку
 *     tags: [Attacks]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - id
 *             properties:
 *               id:
 *                 type: string
 *                 format: uuid
 *                 example: "123e4567-e89b-12d3-a456-426614174000"
 *               name:
 *                 type: string
 *                 example: "Updated DDoS Attack"
 *               frequency:
 *                 type: string
 *                 example: "Medium"
 *               danger:
 *                 type: string
 *                 example: "High"
 *               attack_type:
 *                 type: string
 *                 example: "Application"
 *     responses:
 *       200:
 *         description: Атака успешно обновлена
 *       404:
 *         description: Атака не найдена
 *       500:
 *         description: Ошибка при обновлении атаки
 */
router.patch("/", updateAttackController);

/**
 * @swagger
 * /attack:
 *   delete:
 *     summary: Удалить атаку
 *     tags: [Attacks]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - id
 *             properties:
 *               id:
 *                 type: string
 *                 format: uuid
 *                 example: "123e4567-e89b-12d3-a456-426614174000"
 *     responses:
 *       204:
 *         description: Атака успешно удалена
 *       404:
 *         description: Атака не найдена
 *       500:
 *         description: Ошибка при удалении атаки
 */
router.delete("/", deleteAttackController);

export default router;
