import { Router } from "express";
import attackRouter from "./attack";

const rootRouter = Router();

rootRouter.get("/", (_req, res) => {
    res.json({
        message: "Industrial DB API is running!",
        endpoints: {
            docs: "/api-docs",
            health: "/health",
            attacks: "/attack",
        },
        timestamp: new Date().toISOString(),
    });
});

rootRouter.get("/health", (_req, res) => {
    res.status(200).json({
        status: "OK",
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
    });
});

rootRouter.use("/attack", attackRouter);

export default rootRouter;
