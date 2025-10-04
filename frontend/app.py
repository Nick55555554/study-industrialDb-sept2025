import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.header import Header
from ui.forms import AttackForm
from ui.table import AttackTable
from ui.dashboard import Dashboard
from api.client import DDOSApiClient
import threading
from tkinter import messagebox


class DDoSAttackApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("DDoS Attack Manager")
        self.window.geometry("1400x800")
        self.window.minsize(1200, 700)

        # Инициализация API клиента
        self.api_client = DDOSApiClient()

        # Загрузка данных с сервера
        self.attacks = []

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

        # Enum значения для формы (только разрешенные типы)
        self.frequency_levels = ["low", "medium", "high", "very_high", "continuous"]
        self.danger_levels = ["low", "medium", "high", "critical"]  # Только эти значения
        self.attack_types = ["volumetric", "protocol", "application", "amplification"]  # Только эти значения
        self.protocols = ["tcp", "udp", "dns", "http", "https", "icmp"]

        self.current_edit_id = None
        self.setup_ui()

        # Загружаем данные при запуске
        self.refresh_attacks()

    def setup_ui(self):
        """Создание интерфейса с тремя вкладками"""
        # Основной фрейм
        main_frame = ctk.CTkFrame(self.window, fg_color=self.colors["dark_bg"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Создание layout
        self.create_layout(main_frame)

    def create_layout(self, parent):
        """Создание основного layout"""
        # Основной контейнер
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=0, pady=0)

        # Инициализация компонентов UI
        self.sidebar = Sidebar(container, self)
        self.header = Header(container, self)
        self.content_frame = self.create_content_frame(container)

        # Показываем главную страницу по умолчанию
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

    def show_dashboard(self):
        """Показать главную страницу"""
        self.clear_content()
        self.header.set_title("Main Dashboard")
        Dashboard(self.content_frame, self)

    def show_attack_form(self):
        """Показать форму добавления атаки"""
        self.clear_content()
        self.header.set_title("Add New Attack")
        AttackForm(self.content_frame, self)

    def show_attacks_list(self):
        """Показать таблицу с атаками"""
        self.clear_content()
        self.header.set_title("View Attacks Table")
        AttackTable(self.content_frame, self)

    def refresh_attacks(self):
        """Обновление списка атак с сервера"""

        def refresh_thread():
            try:
                attacks = self.api_client.get_all_attacks()
                self.window.after(0, lambda: self.on_attacks_loaded(attacks))
            except Exception as e:
                self.window.after(0, lambda: self.show_error(f"Failed to refresh attacks: {e}"))

        thread = threading.Thread(target=refresh_thread)
        thread.daemon = True
        thread.start()

    def on_attacks_loaded(self, attacks):
        """Обработка загруженных атак"""
        self.attacks = attacks
        self.update_stats()

    def update_stats(self):
        """Обновление статистики"""
        if hasattr(self, 'sidebar'):
            self.sidebar.update_stats()
        if hasattr(self, 'header'):
            self.header.update_stats()

    def show_error(self, message):
        """Показ ошибки"""
        messagebox.showerror("Error", message)

    def show_success(self, message):
        """Показ успеха"""
        messagebox.showinfo("Success", message)

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()