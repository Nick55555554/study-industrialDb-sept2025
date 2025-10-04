import customtkinter as ctk


class Header:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)

    def setup_ui(self, parent):
        """Создание заголовка"""
        header = ctk.CTkFrame(parent, fg_color=self.app.colors["card_bg"], height=70)
        header.pack(fill="x", padx=0, pady=(0, 10))
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", padx=20, pady=15)

        self.title_label = ctk.CTkLabel(header_content, text="DDoS Attacks",
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color=self.app.colors["text_light"])
        self.title_label.pack(side="left")

    def set_title(self, title):
        """Установка заголовка"""
        self.title_label.configure(text=title)

    def update_stats(self):
        """Обновление статистики (упрощено)"""
        pass