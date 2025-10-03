import { Request, Response, NextFunction } from 'express';
import { httpLogger, errorLogger } from '../logger';

export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
    const start = Date.now();

    // Логируем входящий запрос
    httpLogger.info('Incoming request', {
        method: req.method,
        url: req.url,
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        query: req.query,
        body: req.method !== 'GET' ? req.body : undefined
    });

    // Перехватываем ответ для логирования
    const originalSend = res.send;
    res.send = function(body: any) {
        const duration = Date.now() - start;

        httpLogger.info('Request completed', {
            method: req.method,
            url: req.url,
            statusCode: res.statusCode,
            duration: `${duration}ms`,
            contentLength: res.get('Content-Length'),
            userId: (req as any).user?.id // если есть аутентификация
        });

        return originalSend.call(this, body);
    };

    next();
};

export const errorLoggerMiddleware = (error: any, req: Request, res: Response, next: NextFunction) => {
    errorLogger.error('Unhandled error', {
        method: req.method,
        url: req.url,
        ip: req.ip,
        error: {
            message: error.message,
            stack: error.stack,
            code: error.code,
            details: error.details
        },
        body: req.body,
        query: req.query
    });

    next(error);
};