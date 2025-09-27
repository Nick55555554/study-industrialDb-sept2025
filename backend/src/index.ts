import dotenv from "dotenv";
import express from "express";
import cors from "cors";
import { dbMiddleware } from "./middlewares";
import rootRouter from "./routes";
import helmet from "helmet";
import db from "./db";
import swaggerJsdoc from "swagger-jsdoc";
import swaggerUi from "swagger-ui-express";

dotenv.config();

const app = express();

const swaggerOptions = {
    definition: {
        openapi: "3.0.0",
        info: {
            title: "Industrial DB API",
            version: "1.0.0",
            description: "API для промышленной базы данных",
        },
        servers: [
            {
                url: `http://localhost:${process.env.PORT || 8000}`,
                description: "Development server",
            },
        ],
    },
    apis: ["./src/routes/**/*.ts"],
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

db.raw("SELECT 1")
    .then(() => {
        console.log("Database connected successfully");
    })
    .catch((error) => {
        console.error("Database connection failed:", error);
        process.exit(1);
    });

app.use(cors());
app.use(helmet());
app.use(express.json());
app.use(dbMiddleware);
app.use(rootRouter);

const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Swagger docs available at http://localhost:${PORT}/api-docs`);
});
