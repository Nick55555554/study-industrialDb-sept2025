import { Router } from "express";
import { createAttackController } from "../../controllers/attack";

const router = Router()

router.post('/attack', createAttackController)

export default router