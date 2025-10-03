import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.header import Header
from ui.forms import AttackForm
from ui.table import AttackTable
from ui.dashboard import Dashboard
from ui.settings import Settings
from api.client import DDOSApiClient
from utils.helpers import generate_id, get_current_timestamp
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
            return self.api_client.get_all_attacks()
        except Exception as e:
            self.show_error(f"Failed to load attacks from server: {e}")
            return []

    def check_database_connection(self):
        """Проверка подключения к БД"""

        def check():
            try:
                status = self.api_client.check_database_status()
                print(f"✅ Database status: {status}")
            except Exception as e:
                self.show_error(f"❌ Database connection failed: {e}")

        # Запускаем в отдельном потоке чтобы не блокировать UI
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

        # Показываем дашборд по умолчанию
        self.show_dashboard()

    def create_content_frame(self, parent):
        """Создание контентной области"""
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        return content_frame

    def clear_content(self):
        """Очистить контентную область"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_attack_form(self):
        """Показать форму создания атаки"""
        self.clear_content()
        self.header.set_title("Create New Attack")
        AttackForm(self.content_frame, self)

    def show_attacks_list(self):
        """Показать список атак"""
        self.clear_content()
        self.header.set_title("All Attacks")
        AttackTable(self.content_frame, self)

    def show_dashboard(self):
        """Показать дашборд"""
        self.clear_content()
        self.header.set_title("Attack Dashboard")
        Dashboard(self.content_frame, self)

    def show_settings(self):
        """Показать настройки"""
        self.clear_content()
        self.header.set_title("Settings")
        Settings(self.content_frame, self)

    def save_data(self):
        """Сохранение данных (теперь через API)"""
        # Данные сохраняются непосредственно при операциях через API
        pass

    def refresh_attacks(self):
        """Обновление списка атак с сервера"""
        try:
            self.attacks = self.api_client.get_all_attacks()
            self.update_stats()
        except Exception as e:
            self.show_error(f"Failed to refresh attacks: {e}")

    def update_stats(self):
        """Обновление статистики во всех компонентах"""
        self.sidebar.update_stats()
        self.header.update_stats()

    def show_error(self, message):
        """Показ ошибки"""
        messagebox.showerror("Error", message)

    def show_success(self, message):
        """Показ успеха"""
        messagebox.showinfo("Success", message)

    # ДОБАВЛЕННЫЕ МЕТОДЫ ДЛЯ СОВМЕСТИМОСТИ
    def get_current_timestamp(self):
        """Получение текущей даты и времени"""
        from utils.helpers import get_current_timestamp
        return get_current_timestamp()

    def generate_id(self):
        """Генерация UUID"""
        from utils.helpers import generate_id
        return generate_id()

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

    def initialize_database(self):
        """Автоматическая инициализация базы данных при запуске"""
        try:
            # Проверяем статус БД
            status = self.api_client.check_database_status()
            if not status.get('data', {}).get('tablesExist', False):
                print("🔄 Tables don't exist. Initializing database...")
                result = self.api_client.initialize_database()
                print("✅ Database initialized successfully")
            else:
                print("✅ Database is ready")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            # Показываем ошибку пользователю
            self.show_error(f"Database initialization failed: {e}")