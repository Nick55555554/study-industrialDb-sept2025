import { Attack, AttackData } from "../../db/models/attack"
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


export const createTableController = async (req: Request, res: Response) => {
    try {
        await db.schema.createTable('attacks', (table) => {
            table.uuid('id').primary().defaultTo(db.raw('gen_random_uuid()'));
            table.string('name').notNullable();
            table.string('frequency').notNullable();
            table.string('danger').notNullable();
            table.string('attack_type').notNullable();
            table.timestamp('created_at').defaultTo(db.fn.now());
            table.timestamp('updated_at').defaultTo(db.fn.now());
        });

        res.status(200).json({
            success: true,
            message: 'Table created successfully'
        });
    } catch (error) {
        console.error('Table creation error:', error);
        res.status(500).json({
            success: false,
            message: 'Failed to create table'
        });
    }
};


export const deleteAttackController = async (req: Request, res: Response) => {
    const attackData = req.body;
    try{
        await AttackRepository.delById(attackData.id, db);
    }
    catch (error){
        throw error;
    }
    return res.status(204).send();
}

export const updateAttackController = async (req: Request, res: Response) => {
    const attackData = req.body;
    try {
        const { id } = attackData.id;
        const updateData = req.body as AttackData;
        await AttackRepository.update(id, updateData);
        return res.status(200).send();
    }
    catch(error){

    }

}
export const readAllAttacksController = async (req: Request, res: Response) => {
    try{
        const allAttacks = await AttackRepository.findAllAttacks(db);
        return res.status(200).json({data: allAttacks})
    }
    catch (error){
        throw error;
    }
}



//200


