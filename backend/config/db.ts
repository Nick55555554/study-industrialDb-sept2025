import { knex, Knex } from "knex";
import dotenv from "dotenv";

dotenv.config();

interface DatabaseConfig {
    development: Knex.Config;
}

const config: DatabaseConfig = {
    development: {
        client: "pg",
        connection: {
            host: process.env.DB_HOST || "localhost",
            port: parseInt(process.env.DB_PORT || "5432"),
            database: process.env.DB_NAME || "myapp_dev",
            user: process.env.DB_USER || "postgres",
            password: process.env.DB_PASSWORD || "password",
        },
    },
};
export default config["development"];
