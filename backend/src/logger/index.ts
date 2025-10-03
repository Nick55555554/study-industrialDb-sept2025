import winston from 'winston';
import 'winston-daily-rotate-file';

// Создаем директорию для логов если не существует
import fs from 'fs';
import path from 'path';

const logDir = 'logs';
if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir);
}

// Формат логов
const logFormat = winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
);

// Формат для консоли
const consoleFormat = winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.colorize(),
    winston.format.printf(({ timestamp, level, message, stack, ...meta }) => {
        let log = `${timestamp} [${level}]: ${message}`;

        if (stack) {
            log += `\n${stack}`;
        }

        if (Object.keys(meta).length > 0) {
            log += `\n${JSON.stringify(meta, null, 2)}`;
        }

        return log;
    })
);

// Создаем логгер
const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: logFormat,
    defaultMeta: { service: 'ddos-api' },
    transports: [
        // Файл для всех логов
        new winston.transports.DailyRotateFile({
            filename: path.join(logDir, 'combined-%DATE%.log'),
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d'
        }),

        // Файл для ошибок
        new winston.transports.DailyRotateFile({
            filename: path.join(logDir, 'error-%DATE%.log'),
            datePattern: 'YYYY-MM-DD',
            level: 'error',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '30d'
        }),

        // Файл для HTTP запросов
        new winston.transports.DailyRotateFile({
            filename: path.join(logDir, 'http-%DATE%.log'),
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d'
        }),

        // Файл для базы данных
        new winston.transports.DailyRotateFile({
            filename: path.join(logDir, 'database-%DATE%.log'),
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d'
        })
    ]
});

// Добавляем консольный вывод в development
if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: consoleFormat
    }));
}

// Специализированные логгеры
export const httpLogger = logger.child({ module: 'http' });
export const dbLogger = logger.child({ module: 'database' });
export const appLogger = logger.child({ module: 'application' });
export const errorLogger = logger.child({ module: 'error' });

export default logger;