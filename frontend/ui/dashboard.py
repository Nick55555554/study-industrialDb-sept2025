import customtkinter as ctk
from typing import List, Dict, Any

class Dashboard:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)

    def setup_ui(self, parent):
        """Настройка дашборда"""
        dashboard_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(
            dashboard_frame,
            text="Attack Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.app.colors["text_light"]
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # Секция статистики
        self.create_stats_section(dashboard_frame)

        # Секция последних атак
        self.create_recent_attacks_section(dashboard_frame)

    def create_stats_section(self, parent):
        """Создание секции статистики"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 30))

        ctk.CTkLabel(
            stats_frame,
            text="Overview Statistics",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", pady=(0, 15))

        # Контейнер для карточек статистики
        cards_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        cards_container.pack(fill="x")

        # Статистические карточки
        stats_cards = [
            ("Total Attacks", self.get_total_attacks(), "#e76f51"),
            ("Critical Attacks", self.get_critical_attacks(), "#e63946"),
            ("Active Attacks", self.get_active_attacks(), "#2a9d8f"),
            ("Total Targets", self.get_total_targets(), "#f4a261")
        ]

        for i, (title, value, color) in enumerate(stats_cards):
            card = self.create_stat_card(cards_container, title, value, color)
            card.grid(row=0, column=i, padx=(0, 15), sticky="ew")
            cards_container.columnconfigure(i, weight=1)

    def create_stat_card(self, parent, title, value, color):
        """Создание карточки статистики"""
        card = ctk.CTkFrame(parent, fg_color=self.app.colors["card_bg"], height=120)
        card.pack_propagate(False)

        # Контент карточки
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color=self.app.colors["text_muted"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            content_frame,
            text=str(value),
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=color
        ).pack(anchor="w", pady=(10, 0))

        return card

    def create_recent_attacks_section(self, parent):
        """Создание секции последних атак"""
        attacks_frame = ctk.CTkFrame(parent, fg_color="transparent")
        attacks_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            attacks_frame,
            text="Recent Attacks",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", pady=(0, 15))

        # Таблица последних атак
        self.create_attacks_table(attacks_frame)

    def create_attacks_table(self, parent):
        """Создание таблицы атак"""
        table_frame = ctk.CTkFrame(parent, fg_color=self.app.colors["card_bg"])
        table_frame.pack(fill="both", expand=True)

        # Заголовки таблицы
        headers = ["Name", "Type", "Danger", "Frequency", "Targets", "Date"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                table_frame,
                text=header,
                font=ctk.CTkFont(weight="bold"),
                text_color=self.app.colors["text_muted"]
            )
            label.grid(row=0, column=i, padx=15, pady=15, sticky="w")

        # Данные атак
        self.populate_attacks_table(table_frame)

    def populate_attacks_table(self, parent):
        """Заполнение таблицы атаками"""
        attacks_to_show = self.app.attacks[:5]  # Показываем последние 5 атак

        for row, attack in enumerate(attacks_to_show, start=1):
            if not isinstance(attack, dict):
                continue

            # Безопасно извлекаем данные
            name = attack.get("name", "Unknown")
            attack_type = attack.get("attack_type", "Unknown")
            danger = attack.get("danger", "Unknown")
            frequency = attack.get("frequency", "Unknown")

            # Безопасно считаем цели
            targets_count = len(attack.get("targets", []))

            # Дата
            created_date = attack.get("created_at", "Unknown")
            if created_date != "Unknown":
                created_date = created_date[:10]  # Берем только дату

            data = [name, attack_type, danger, frequency, f"{targets_count} targets", created_date]

            for col, value in enumerate(data):
                label = ctk.CTkLabel(
                    parent,
                    text=value,
                    font=ctk.CTkFont(size=12)
                )
                label.grid(row=row, column=col, padx=15, pady=10, sticky="w")

    # Методы для безопасного получения статистики
    def get_total_attacks(self):
        """Безопасное получение общего количества атак"""
        if not hasattr(self.app, 'attacks') or not isinstance(self.app.attacks, list):
            return 0
        return len(self.app.attacks)

    def get_critical_attacks(self):
        """Безопасное получение количества критических атак"""
        if not hasattr(self.app, 'attacks') or not isinstance(self.app.attacks, list):
            return 0

        critical_count = 0
        for attack in self.app.attacks:
            if isinstance(attack, dict) and attack.get("danger") == "critical":
                critical_count += 1
        return critical_count

    def get_active_attacks(self):
        """Безопасное получение количества активных атак"""
        if not hasattr(self.app, 'attacks') or not isinstance(self.app.attacks, list):
            return 0

        active_count = 0
        for attack in self.app.attacks:
            if isinstance(attack, dict):
                # Если статус явно указан как active, или статуса нет (считаем активной)
                if attack.get("status") == "active" or "status" not in attack:
                    active_count += 1
        return active_count

    def get_total_targets(self):
        """Безопасное получение общего количества целей"""
        if not hasattr(self.app, 'attacks') or not isinstance(self.app.attacks, list):
            return 0

        total_targets = 0
        for attack in self.app.attacks:
            if isinstance(attack, dict) and "targets" in attack:
                total_targets += len(attack["targets"])
        return total_targets