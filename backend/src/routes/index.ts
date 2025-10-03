import { Router } from 'express';
import attackRoutes from './attackRoutes';
import filterRoutes from './filterRoutes';

const router = Router();

router.use('/', attackRoutes);
router.use('/', filterRoutes);

export default router;