import logging
import os


class AppLogger:
    def __init__(self, log_file: str = "logs/app.log"):
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self):
        """Настройка логгера"""
        # Создаем папку для логов если не существует
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('DDoSApp')

    def log_info(self, message: str):
        """Логирование информационного сообщения"""
        self.logger.info(message)

    def log_error(self, message: str):
        """Логирование ошибки"""
        self.logger.error(message)

    def log_warning(self, message: str):
        """Логирование предупреждения"""
        self.logger.warning(message)

    def log_database_operation(self, operation: str, success: bool = True):
        """Логирование операции с БД"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"DB_OPERATION: {operation} - {status}")

    def log_connection_attempt(self, endpoint: str, success: bool = True):
        """Логирование попытки подключения"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"CONNECTION: {endpoint} - {status}")