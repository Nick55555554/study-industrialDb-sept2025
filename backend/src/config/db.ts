import { Knex } from "knex";

// console.log(process.env.DB_HOST);
// console.log('🔍 Environment variables:');
// console.log('DB_HOST:', process.env.DB_HOST);
// console.log('DB_PORT:', process.env.DB_PORT);
// console.log('DB_NAME:', process.env.DB_NAME);
// console.log('DB_USER:', process.env.DB_USER);
// console.log('DB_PASSWORD:', process.env.DB_PASSWORD);
// console.log('DB_PASSWORD type:', typeof process.env.DB_PASSWORD);
console.log('PORT:', process.env.PORT);
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
