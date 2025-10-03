import customtkinter as ctk
from datetime import datetime


class Header:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)

    def setup_ui(self, parent):
        """Создание заголовка"""
        header = ctk.CTkFrame(parent, fg_color=self.app.colors["primary"], height=80)
        header.pack(fill="x", padx=5, pady=(0, 5))
        header.pack_propagate(False)

        # Основной контейнер
        main_container = ctk.CTkFrame(header, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Заголовок и статистика в одной строке
        title_stats_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_stats_frame.pack(fill="x")

        # Заголовок слева
        self.title_label = ctk.CTkLabel(
            title_stats_frame,
            text="Attack Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.app.colors["text_light"]
        )
        self.title_label.pack(side="left")

        # Статистика справа
        stats_frame = ctk.CTkFrame(title_stats_frame, fg_color="transparent")
        stats_frame.pack(side="right")

        # Создаем labels для статистики
        self.total_attacks_label = ctk.CTkLabel(
            stats_frame,
            text="Total Attacks: 0",
            font=ctk.CTkFont(size=14),
            text_color=self.app.colors["text_light"]
        )
        self.total_attacks_label.pack(side="right", padx=(20, 0))

        self.total_targets_label = ctk.CTkLabel(
            stats_frame,
            text="Total Targets: 0",
            font=ctk.CTkFont(size=14),
            text_color=self.app.colors["text_light"]
        )
        self.total_targets_label.pack(side="right", padx=(20, 0))

        # Обновляем статистику
        self.update_stats()

    def set_title(self, title):
        """Установка заголовка"""
        self.title_label.configure(text=title)

    def update_stats(self):
        """Обновление статистики в заголовке"""
        try:
            # Проверяем, что attacks существует и это список
            if not hasattr(self.app, 'attacks') or not isinstance(self.app.attacks, list):
                self.total_attacks_label.configure(text="Total Attacks: 0")
                self.total_targets_label.configure(text="Total Targets: 0")
                return

            total_attacks = len(self.app.attacks)

            # Безопасный подсчет целей
            total_targets = 0
            for attack in self.app.attacks:
                if isinstance(attack, dict) and "targets" in attack:
                    total_targets += len(attack["targets"])

            # Обновляем labels
            self.total_attacks_label.configure(text=f"Total Attacks: {total_attacks}")
            self.total_targets_label.configure(text=f"Total Targets: {total_targets}")

        except Exception as e:
            print(f"Error updating header stats: {e}")
            # Устанавливаем значения по умолчанию при ошибке
            if hasattr(self, 'total_attacks_label'):
                self.total_attacks_label.configure(text="Total Attacks: Error")
            if hasattr(self, 'total_targets_label'):
                self.total_targets_label.configure(text="Total Targets: Error")