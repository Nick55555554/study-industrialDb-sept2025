import customtkinter as ctk
from tkinter import ttk
from datetime import datetime

class AttackTable:
    def __init__(self, parent, app):
        self.app = app
        self.tree = None
        self.setup_ui(parent)
        self.refresh_table()
    
    def setup_ui(self, parent):
        """Создание таблицы для отображения атак"""
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Стиль таблицы
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                       background=self.app.colors["card_bg"],
                       foreground=self.app.colors["text_light"],
                       fieldbackground=self.app.colors["card_bg"],
                       borderwidth=0,
                       rowheight=30)
        style.configure("Treeview.Heading",
                       background="#3a3a5a",
                       foreground=self.app.colors["text_light"],
                       relief="flat",
                       font=('Arial', 11, 'bold'))
        style.map("Treeview", background=[('selected', '#1f6aa5')])
        
        columns = ("ID", "Name", "Frequency", "Danger", "Type", "Source IPs", "Ports", "Targets", "Created", "Actions")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
        
        # Настройка колонок
        column_widths = {
            "ID": 80, "Name": 150, "Frequency": 100, "Danger": 100, "Type": 120,
            "Source IPs": 150, "Ports": 100, "Targets": 100, "Created": 120, "Actions": 120
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязка событий
        self.tree.bind("<Double-1>", self.on_double_click)
    
    def refresh_table(self):
        """Обновление таблицы"""
        if not self.tree:
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for attack in self.app.attacks:
            # Сокращенные данные для таблицы
            source_ips_preview = ", ".join(attack["source_ips"][:2]) + ("..." if len(attack["source_ips"]) > 2 else "")
            ports_preview = ", ".join(map(str, attack["affected_ports"][:3])) + ("..." if len(attack["affected_ports"]) > 3 else "")
            targets_count = len(attack["targets"])
            created_date = datetime.fromisoformat(attack["created_at"]).strftime("%Y-%m-%d")
            
            item = self.tree.insert("", "end", values=(
                attack["id"][:8] + "...",
                attack["name"],
                attack["frequency"],
                attack["danger"],
                attack["attack_type"],
                source_ips_preview,
                ports_preview,
                f"{targets_count} targets",
                created_date,
                "Edit/Delete"
            ))
            
            # Привязка контекстного меню
            self.tree.bind("<Button-3>", lambda e, aid=attack["id"]: self.show_context_menu(e, aid))
    
    def on_double_click(self, event):
        """Обработка двойного клика"""
        if self.tree:
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                attack_id = item["values"][0]
                self.edit_attack(attack_id)
    
    def show_context_menu(self, event, attack_id):
        """Показ контекстного меню"""
        menu = ctk.CTkToplevel(self.app.window)
        menu.geometry(f"+{event.x_root}+{event.y_root}")
        menu.overrideredirect(True)
        menu.attributes("-topmost", True)
        
        edit_btn = ctk.CTkButton(menu, text="✏️ Edit Attack", 
                               command=lambda: [self.edit_attack(attack_id), menu.destroy()])
        edit_btn.pack(fill="x")
        
        delete_btn = ctk.CTkButton(menu, text="🗑️ Delete Attack", 
                                 command=lambda: [self.delete_attack(attack_id), menu.destroy()],
                                 fg_color=self.app.colors["danger"], hover_color="#e55a5a")
        delete_btn.pack(fill="x")
        
        def close_menu(e):
            menu.destroy()
        menu.bind("<FocusOut>", close_menu)
        menu.focus_set()
    
    def edit_attack(self, attack_id):
        """Редактирование атаки"""
        self.app.current_edit_id = attack_id
        self.app.show_attack_form()
        
        # Заполнение формы данными атаки
        attack = next((a for a in self.app.attacks if a["id"] == attack_id), None)
        if attack:
            form = self.app.content_frame.winfo_children()[0]
            if hasattr(form, 'fill_form_data'):
                form.fill_form_data(attack)
    
    def delete_attack(self, attack_id):
        """Удаление атаки"""
        attack_name = next((a["name"] for a in self.app.attacks if a["id"] == attack_id), "Unknown")
        self.app.attacks = [attack for attack in self.app.attacks if attack["id"] != attack_id]
        self.app.save_data()
        self.refresh_table()
        self.app.update_stats()
        self.show_success(f"Attack '{attack_name}' deleted successfully!")
    
    def show_success(self, message):
        """Показ успеха"""
        print(f"✅ {message}")