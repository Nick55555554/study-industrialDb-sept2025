import { Request, Response, NextFunction } from "express";
import db from "../db/connection";

declare global {
    namespace Express {
        interface Request {
            db: typeof db;
        }
    }
}

export const dbMiddleware = (
    req: Request,
    _res: Response,
    next: NextFunction
) => {
    req.db = db;
    next();
};
