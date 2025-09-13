import { AttackData } from "../../db/models/attack"
import e, {Request, Response} from 'express'
import { AttackRepository } from "../../repositories/attack-repository";
import db from '../../db/connection'
type CreateAttackBody = Omit<AttackData, 'id'>

export const createAttackController = async (
    req: Request<CreateAttackBody>,
    res: Response<unknown>,
) => {
    const attackData = req.body;

    try {
        
        await AttackRepository.create(attackData, db);
    } catch (error) {
        throw error;
    }

    return res.status(201).send()
}
