import { Router } from "express";
import attackRouter from './attack'

const rootRouter = Router();


rootRouter.use('attack', attackRouter)

export default rootRouter;