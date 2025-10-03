import { Router } from 'express';
import attackRoutes from './attackRoutes';
import filterRoutes from './filterRoutes';

const router = Router();

router.use('/', filterRoutes);
router.use('/', attackRoutes);


export default router;