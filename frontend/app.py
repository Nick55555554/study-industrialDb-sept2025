import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.header import Header
from ui.main_window import MainWindow
from ui.dashboard import Dashboard
from ui.settings import Settings
from api.client import DDOSApiClient
from utils.logger import AppLogger
import threading
from tkinter import messagebox
from typing import List, Dict, Any


class DDoSAttackApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("DDoS Attack Manager - Security Dashboard")
        self.window.geometry("1600x900")
        self.window.minsize(1400, 800)

        # Инициализация API клиента
        self.api_client = DDOSApiClient()

        # Инициализация логгера
        self.logger = AppLogger()

        # Проверка и инициализация БД при запуске
        self.initialize_database()

        # Загрузка данных с сервера
        self.attacks = self.load_attacks_from_server()

        # Цветовая схема
        self.colors = {
            "primary": "#2b5876",
            "secondary": "#4e4376",
            "accent": "#ff6b6b",
            "success": "#4ecdc4",
            "warning": "#ffd166",
            "danger": "#ff6b6b",
            "dark_bg": "#1a1a2e",
            "card_bg": "#16213e",
            "text_light": "#ffffff",
            "text_muted": "#b0b0b0"
        }

        # Enum значения
        self.frequency_levels = ["low", "medium", "high", "very_high", "continuous"]
        self.danger_levels = ["low", "medium", "high", "critical"]
        self.attack_types = ["amplification", "protocol", "application", "volumetric", "fragmentation"]
        self.protocols = ["tcp", "udp", "dns", "http", "https", "icmp"]

        self.current_edit_id = None
        self.setup_ui()

        # Проверка подключения к БД при запуске
        self.check_database_connection()

    def load_attacks_from_server(self) -> List[Dict[str, Any]]:
        """Загрузка атак с сервера"""
        try:
            self.logger.log_info("Загрузка данных атак с сервера...")
            attacks = self.api_client.get_all_attacks()
            self.logger.log_info(f"Успешно загружено {len(attacks)} атак")
            return attacks
        except Exception as e:
            self.logger.log_error(f"Ошибка загрузки атак с сервера: {e}")
            self.show_error(f"Ошибка загрузки данных с сервера: {e}")
            return []

    def check_database_connection(self):
        """Проверка подключения к БД"""

        def check():
            try:
                self.logger.log_info("Проверка подключения к базе данных...")
                status = self.api_client.check_database_status()
                if status.get('success'):
                    tables_exist = status.get('data', {}).get('tablesExist', False)
                    status_msg = "существуют" if tables_exist else "не существуют"
                    self.logger.log_info(f"Таблицы в БД: {status_msg}")
                else:
                    self.logger.log_warning("Не удалось проверить статус БД")
            except Exception as e:
                self.logger.log_error(f"Ошибка проверки подключения к БД: {e}")

        thread = threading.Thread(target=check)
        thread.daemon = True
        thread.start()

    def setup_ui(self):
        """Создание улучшенного интерфейса"""
        # Основной фрейм с градиентным фоном
        main_frame = ctk.CTkFrame(self.window, fg_color=self.colors["dark_bg"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Создание layout с sidebar и main content
        self.create_layout(main_frame)

    def create_layout(self, parent):
        """Создание основного layout с sidebar"""
        # Основной контейнер
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=0, pady=0)

        # Инициализация компонентов UI
        self.sidebar = Sidebar(container, self)
        self.header = Header(container, self)
        self.content_frame = self.create_content_frame(container)

        # Показываем главное окно по умолчанию
        self.show_main_window()

    def create_content_frame(self, parent):
        """Создание контентной области"""
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        return content_frame

    def clear_content(self):
        """Очистить контентную область"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_window(self):
        """Показать главное окно с кнопками"""
        self.clear_content()
        self.header.set_title("Главное окно")
        from ui.main_window import MainWindow
        MainWindow(self.content_frame, self)

    def show_attack_form(self):
        """Показать форму создания атаки (старая логика для совместимости)"""
        self.clear_content()
        self.header.set_title("Create New Attack")
        from ui.attack_form import AttackForm
        AttackForm(self.content_frame, self)

    def show_attacks_list(self):
        """Показать список атак (старая логика для совместимости)"""
        self.clear_content()
        self.header.set_title("All Attacks")
        from ui.attack_table import AttackTable
        AttackTable(self.content_frame, self)

    def show_dashboard(self):
        """Показать дашборд"""
        self.clear_content()
        self.header.set_title("Attack Dashboard")
        from ui.dashboard import Dashboard
        Dashboard(self.content_frame, self)

    def show_settings(self):
        """Показать настройки"""
        self.clear_content()
        self.header.set_title("Settings")
        from ui.settings import Settings
        Settings(self.content_frame, self)

    def refresh_attacks(self):
        """Обновление списка атак с сервера"""
        try:
            self.logger.log_info("Обновление списка атак...")
            self.attacks = self.api_client.get_all_attacks()
            self.update_stats()
            self.logger.log_info("Список атак успешно обновлен")
        except Exception as e:
            self.logger.log_error(f"Ошибка обновления атак: {e}")
            self.show_error(f"Ошибка обновления данных: {e}")

    def update_stats(self):
        """Обновление статистики во всех компонентах"""
        if hasattr(self, 'sidebar'):
            self.sidebar.update_stats()
        if hasattr(self, 'header'):
            self.header.update_stats()

    def show_error(self, message):
        """Показ ошибки"""
        self.logger.log_error(f"Ошибка UI: {message}")
        messagebox.showerror("Ошибка", message)

    def show_success(self, message):
        """Показ успеха"""
        self.logger.log_info(f"Успех: {message}")
        messagebox.showinfo("Успех", message)

    def run(self):
        """Запуск приложения"""
        self.logger.log_info("Запуск приложения DDoS Attack Manager")
        self.window.mainloop()

    def initialize_database(self):
        """Автоматическая инициализация базы данных при запуске"""
        try:
            self.logger.log_info("Проверка и инициализация базы данных...")

            # Всегда пытаемся инициализировать БД
            # Если таблицы уже существуют - это нормально
            result = self.api_client.initialize_database()

            if result.get('success') or result.get('status') == 'already_exists':
                self.logger.log_database_operation("CREATE_SCHEMA", True)
                if result.get('status') == 'already_exists':
                    self.logger.log_info("Таблицы уже существуют в базе данных")
                else:
                    self.logger.log_info("База данных успешно инициализирована")
            else:
                self.logger.log_database_operation("CREATE_SCHEMA", False)
                self.logger.log_warning("Не удалось инициализировать базу данных")

        except Exception as e:
            # Если ошибка связана с тем, что таблицы уже существуют - это нормально
            if "409" in str(e) or "already exists" in str(e).lower():
                self.logger.log_database_operation("CREATE_SCHEMA", True)
                self.logger.log_info("Таблицы уже существуют в базе данных")
            else:
                error_msg = f"Ошибка инициализации базы данных: {e}"
                self.logger.log_error(error_msg)
                self.logger.log_database_operation("CREATE_SCHEMA", False)
                # Не показываем ошибку пользователю при запуске
                # self.show_error(error_msg)