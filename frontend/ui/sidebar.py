import customtkinter as ctk
from datetime import datetime


class Sidebar:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)

    def setup_ui(self, parent):
        """Создание боковой панели"""
        sidebar = ctk.CTkFrame(parent, width=280, fg_color=self.app.colors["card_bg"],
                               corner_radius=0)
        sidebar.pack(side="left", fill="y", padx=(0, 5), pady=0)
        sidebar.pack_propagate(False)

        # Логотип и заголовок
        self.create_logo_section(sidebar)

        # Навигация
        self.create_navigation_section(sidebar)

        # Статистика
        self.create_stats_section(sidebar)

    def create_logo_section(self, parent):
        """Создание секции с логотипом"""
        logo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=30)

        ctk.CTkLabel(logo_frame, text="🛡️", font=ctk.CTkFont(size=28)).pack()
        ctk.CTkLabel(logo_frame, text="DDoS Manager",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=self.app.colors["text_light"]).pack(pady=(5, 0))
        ctk.CTkLabel(logo_frame, text="Security Dashboard",
                     font=ctk.CTkFont(size=12),
                     text_color=self.app.colors["text_muted"]).pack()

    def create_navigation_section(self, parent):
        """Создание секции навигации"""
        nav_frame = ctk.CTkFrame(parent, fg_color="transparent")
        nav_frame.pack(fill="x", padx=15, pady=20)

        # Кнопки навигации
        nav_buttons = [
            ("📊 Attack Dashboard", self.app.show_dashboard),
            ("➕ New Attack", self.app.show_attack_form),
            ("📋 All Attacks", self.app.show_attacks_list),
            ("⚙️ Settings", self.app.show_settings)
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(nav_frame, text=text, command=command,
                                fg_color="transparent", hover_color="#2a2a4a",
                                anchor="w", font=ctk.CTkFont(size=14))
            btn.pack(fill="x", pady=5)

    def create_stats_section(self, parent):
        """Создание секции статистики"""
        stats_frame = ctk.CTkFrame(parent, fg_color="#2a2a4a")
        stats_frame.pack(fill="x", padx=15, pady=20)

        ctk.CTkLabel(stats_frame, text="Quick Stats",
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))

        self.stats_label = ctk.CTkLabel(stats_frame, text="", justify="left",
                                        font=ctk.CTkFont(size=12))
        self.stats_label.pack(anchor="w", pady=(0, 10))

        self.update_stats()

    def update_stats(self):
        """Обновление статистики в сайдбаре"""
        try:
            if not hasattr(self.app, 'attacks') or not isinstance(self.app.attacks, list):
                stats_text = "Total Attacks: 0\nCritical: 0\nActive: 0\nLast Updated: " + datetime.now().strftime(
                    "%H:%M")
                self.stats_label.configure(text=stats_text)
                return

            total_attacks = len(self.app.attacks)

            # Безопасный подсчет critical атак
            critical_attacks = 0
            active_attacks = 0
            high_freq_attacks = 0

            for attack in self.app.attacks:
                if isinstance(attack, dict):
                    if attack.get("danger") == "critical":
                        critical_attacks += 1
                    # Если есть поле status, используем его, иначе считаем все активными
                    if attack.get("status") == "active":
                        active_attacks += 1
                    elif "status" not in attack:
                        active_attacks += 1  # Если статуса нет, считаем активной

                    # Подсчет high frequency атак
                    if attack.get("frequency") in ["high", "very_high", "continuous"]:
                        high_freq_attacks += 1

            current_time = datetime.now().strftime("%H:%M")
            stats_text = f"""Total Attacks: {total_attacks}
Critical: {critical_attacks}
Active: {active_attacks}
High Frequency: {high_freq_attacks}
Last Updated: {current_time}"""

            self.stats_label.configure(text=stats_text)

        except Exception as e:
            print(f"Error updating sidebar stats: {e}")
            current_time = datetime.now().strftime("%H:%M")
            stats_text = f"""Total Attacks: Error
Critical: Error
Active: Error
High Frequency: Error
Last Updated: {current_time}"""
            self.stats_label.configure(text=stats_text)