import customtkinter as ctk
from datetime import datetime

class Dashboard:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)
    
    def setup_ui(self, parent):
        """Создание дашборда"""
        dashboard_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Статистика вверху
        self.create_stats_section(dashboard_frame)
        
        # Последние атаки
        self.create_recent_attacks_section(dashboard_frame)
    
    def create_stats_section(self, parent):
        """Создание секции статистики"""
        stats_grid = ctk.CTkFrame(parent, fg_color="transparent")
        stats_grid.pack(fill="x", pady=10)
        
        stats_data = [
            ("Total Attacks", len(self.app.attacks), "#4ecdc4"),
            ("Critical Attacks", len([a for a in self.app.attacks if a["danger"] == "critical"]), "#ff6b6b"),
            ("High Frequency", len([a for a in self.app.attacks if a["frequency"] in ["high", "very_high", "continuous"]]), "#ffd166"),
            ("Total Targets", sum(len(a["targets"]) for a in self.app.attacks), "#2a9d8f")
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            stat_card = self.create_stat_card(stats_grid, title, value, color)
            stat_card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            stats_grid.columnconfigure(i, weight=1)
    
    def create_stat_card(self, parent, title, value, color):
        """Создание карточки статистики"""
        card = ctk.CTkFrame(parent, fg_color=self.app.colors["card_bg"], corner_radius=12, height=100)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(content, text=title, font=ctk.CTkFont(size=12),
                    text_color=self.app.colors["text_muted"]).pack(anchor="w")
        ctk.CTkLabel(content, text=str(value), font=ctk.CTkFont(size=24, weight="bold"),
                    text_color=color).pack(anchor="w", pady=(5, 0))
        
        return card
    
    def create_recent_attacks_section(self, parent):
        """Создание секции последних атак"""
        recent_card = self.create_card(parent, "📈 Recent Attacks")
        recent_frame = ctk.CTkFrame(recent_card, fg_color="transparent")
        recent_frame.pack(fill="x", padx=15, pady=15)
        
        if self.app.attacks:
            recent_attacks = sorted(self.app.attacks, key=lambda x: x['created_at'], reverse=True)[:5]
            for attack in recent_attacks:
                self.create_attack_preview(recent_frame, attack)
        else:
            ctk.CTkLabel(recent_frame, text="No attacks recorded yet", 
                         text_color=self.app.colors["text_muted"]).pack(pady=20)
    
    def create_attack_preview(self, parent, attack):
        """Создание превью атаки для дашборда"""
        preview = ctk.CTkFrame(parent, fg_color="#2a2a4a", corner_radius=8)
        preview.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(preview, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        
        # Основная информация
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(fill="x")
        
        ctk.CTkLabel(info_frame, text=attack["name"], 
                    font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        # Badges
        badges_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        badges_frame.pack(side="right")
        
        danger_color = {
            "low": self.app.colors["success"],
            "medium": self.app.colors["warning"],
            "high": "#ff9a76",
            "critical": self.app.colors["danger"]
        }
        
        danger_badge = ctk.CTkLabel(badges_frame, text=attack["danger"].upper(),
                                   fg_color=danger_color[attack["danger"]],
                                   text_color="white", corner_radius=20,
                                   font=ctk.CTkFont(size=10, weight="bold"))
        danger_badge.pack(side="left", padx=2)
        
        type_badge = ctk.CTkLabel(badges_frame, text=attack["attack_type"],
                                 fg_color="#3a3a5a", text_color="white",
                                 corner_radius=20, font=ctk.CTkFont(size=10))
        type_badge.pack(side="left", padx=2)
    
    def create_card(self, parent, title):
        """Создание карточки с заголовком"""
        card = ctk.CTkFrame(parent, fg_color=self.app.colors["card_bg"], corner_radius=12)
        card.pack(fill="x", padx=5, pady=8)
        
        if title:
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=15, pady=15)
            ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
            
            # Разделитель
            separator = ctk.CTkFrame(card, height=1, fg_color="#3a3a5a")
            separator.pack(fill="x", padx=15)
        
        return card