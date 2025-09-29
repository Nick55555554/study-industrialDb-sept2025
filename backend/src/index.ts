import 'dotenv/config';
import express from 'express';
import attackRoutes from './routes/attackRoutes';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Routes
app.use('/api', attackRoutes);

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    // Импортируем db здесь чтобы избежать циклических зависимостей
    const { db } = await import('./db');
    await db.raw('SELECT 1');

    res.json({
      status: 'OK',
      database: 'connected',
      timestamp: new Date().toISOString()
    });
  } catch (error: any) {
    res.status(500).json({
      status: 'ERROR',
      database: 'disconnected',
      error: error.message
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Database host: ${process.env.DB_HOST}`);
});