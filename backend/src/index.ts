import 'dotenv/config';
import express from 'express';
import routes from './routes';
import { requestLogger, errorLoggerMiddleware } from './middlewares/loggerMiddleware';
import logger from './logger';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(requestLogger);

// Routes
app.use('/api', routes);

// Error handling middleware
app.use(errorLoggerMiddleware);

// Health check
app.get('/health', async (req, res) => {
  try {
    const { db } = await import('./db');
    await db.raw('SELECT 1');

    res.json({
      status: 'OK',
      database: 'connected',
      timestamp: new Date().toISOString()
    });
  } catch (error: any) {
    logger.error('Health check failed', { error: error.message });
    res.status(500).json({
      status: 'ERROR',
      database: 'disconnected',
      error: error.message
    });
  }
});

app.listen(PORT, () => {
  logger.info(`Server started successfully`, {
    port: PORT,
    environment: process.env.NODE_ENV || 'development',
    logLevel: process.env.LOG_LEVEL || 'info'
  });
  console.log(`Server is running on port ${PORT}`);
});

// Обработка неперехваченных исключений
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception', { error: error.message, stack: error.stack });
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection', { reason, promise });
  process.exit(1);
});