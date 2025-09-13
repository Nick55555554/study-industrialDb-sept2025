import knex from "knex";
import dbConfig from "../config/db";

const db = knex(dbConfig);

db.raw("SELECT 1")
    .then(() => {
        console.log("Database connected successfulle");
    })
    .catch((error) => {
        console.error("Database connection failed:", error);
    });

export default db;
