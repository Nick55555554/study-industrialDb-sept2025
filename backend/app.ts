import dotenv from "dotenv";
import express from "express";
import cors from "cors";
import db from "./db/connetion";
import { dbMiddleware } from "./middlewares";

dotenv.config();

const app = express();

app.use(cors());

app.use(express.json());

app.use(dbMiddleware);
