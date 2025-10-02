import { Router } from 'express';
import { AttackController } from '../controllers/attackController';

const router = Router();
const attackController = new AttackController();

// Database management routes
router.post('/database/init', attackController.initializeDatabase);
router.post('/database/reset', attackController.resetDatabase);
router.get('/database/status', attackController.getDatabaseStatus);

// Attack CRUD routes
router.post('/attacks', attackController.createAttack);
router.get('/attacks', attackController.getAllAttacks);
router.get('/attacks/:id', attackController.getAttack);
router.put('/attacks/:id', attackController.updateAttack); // Обновление атаки
router.put('/attacks/:id/with-targets', attackController.updateAttackWithTargets); // Обновление атаки с целями
router.put('/attacks/:id/targets', attackController.updateAttackTargets); // Обновление целей атаки
router.delete('/attacks/:id', attackController.deleteAttack);

// Target routes
router.put('/targets/:id', attackController.updateTarget); // Обновление конкретной цели

export default router;