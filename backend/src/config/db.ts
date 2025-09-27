import { Knex } from "knex";

console.log(process.env.DB_HOST);
const config: Knex.Config = {
    client: "pg",
    connection: {
        host: process.env.DB_HOST as string,
        port: parseInt(process.env.DB_PORT as string),
        database: process.env.DB_NAME as string,
        user: process.env.DB_USER as string,
        password: process.env.DB_PASSWORD as string,
    },
    pool: {
        min: 2,
        max: 10,
    },
    migrations: {
        tableName: "knex_migrations",
    },
};

export default config;
