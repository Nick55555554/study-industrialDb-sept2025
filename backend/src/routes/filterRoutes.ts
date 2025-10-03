import { Router } from 'express';
import { FilterController } from '../controllers/filterController';

const router = Router();
const filterController = new FilterController();

// Комплексная фильтрация
router.get('/attacks/filter', filterController.getAttacksByFilters);

// Статистика
router.get('/attacks/stats', filterController.getAttackStats);

// Доступные фильтры
router.get('/filters/available', filterController.getAvailableFilters);

// Фильтрация по отдельным enum
router.get('/attacks/frequency/:frequency', filterController.getAttacksByFrequency);
router.get('/attacks/danger/:danger', filterController.getAttacksByDanger);
router.get('/attacks/type/:type', filterController.getAttacksByType);
router.get('/attacks/protocol/:protocol', filterController.getAttacksByProtocol);

export default router;