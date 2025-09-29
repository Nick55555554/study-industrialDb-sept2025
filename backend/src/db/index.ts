import knex from "knex";
import dbConfig from "../config/db";


const db = knex(dbConfig);

export { db };
