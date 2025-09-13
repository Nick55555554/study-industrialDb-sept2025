import dotenv from "dotenv";
import express from "express";
import cors from "cors";
import { dbMiddleware } from "./middlewares";
import rootRouter from "./routes";

dotenv.config();

const app = express();

app.use(cors());

app.use(express.json());

app.use(dbMiddleware);

app.use(rootRouter)