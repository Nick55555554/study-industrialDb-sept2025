import customtkinter as ctk

class Header:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)
    
    def setup_ui(self, parent):
        """Создание заголовка"""
        header = ctk.CTkFrame(parent, fg_color=self.app.colors["card_bg"], height=80)
        header.pack(fill="x", padx=0, pady=(0, 10))
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", padx=30, pady=15)
        
        self.title_label = ctk.CTkLabel(header_content, text="Create New Attack",
                                      font=ctk.CTkFont(size=24, weight="bold"),
                                      text_color=self.app.colors["text_light"])
        self.title_label.pack(side="left")
        
        # Статистика в заголовке
        stats_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        stats_frame.pack(side="right")
        
        self.stats_label = ctk.CTkLabel(stats_frame, text="", 
                                      font=ctk.CTkFont(size=12),
                                      text_color=self.app.colors["text_muted"])
        self.stats_label.pack(side="right")
        
        self.update_stats()
    
    def set_title(self, title):
        """Установка заголовка"""
        self.title_label.configure(text=title)
    
    def update_stats(self):
        """Обновление статистики"""
        total_attacks = len(self.app.attacks)
        total_targets = sum(len(a["targets"]) for a in self.app.attacks)
        self.stats_label.configure(text=f"📊 {total_attacks} attacks | 🎯 {total_targets} targets")