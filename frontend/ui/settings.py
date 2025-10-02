import customtkinter as ctk

class Settings:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)
    
    def setup_ui(self, parent):
        """Создание страницы настроек"""
        settings_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        cards = [
            self.create_settings_card(settings_frame, "⚙️ General Settings", [
                ("Theme", "Dark/Light mode toggle"),
                ("Language", "Interface language"),
                ("Auto-save", "Enable auto-save feature")
            ]),
            self.create_settings_card(settings_frame, "🔒 Security", [
                ("Encryption", "Data encryption settings"),
                ("Backup", "Automatic backup configuration"),
                ("Access Control", "User permissions")
            ]),
            self.create_settings_card(settings_frame, "📊 Display", [
                ("Table Density", "Compact/Normal/Comfortable"),
                ("Color Scheme", "Customize colors"),
                ("Notifications", "Alert preferences")
            ])
        ]
        
        for card in cards:
            card.pack(fill="x", pady=8)
    
    def create_settings_card(self, parent, title, settings):
        """Создание карточки настроек"""
        card = self.create_card(parent, title)
        
        for setting, description in settings:
            setting_frame = ctk.CTkFrame(card, fg_color="transparent")
            setting_frame.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(setting_frame, text=setting, font=ctk.CTkFont(weight="bold")).pack(side="left")
            ctk.CTkLabel(setting_frame, text=description, text_color=self.app.colors["text_muted"]).pack(side="left", padx=(10, 0))
            
            ctk.CTkSwitch(setting_frame, text="").pack(side="right")
        
        return card
    
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