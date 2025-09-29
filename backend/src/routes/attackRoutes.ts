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
router.delete('/attacks/:id', attackController.deleteAttack);

export default router;