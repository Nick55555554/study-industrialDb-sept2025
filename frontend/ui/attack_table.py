import customtkinter as ctk
from tkinter import ttk
import threading
from tkinter import messagebox

class AttackTable:
    def __init__(self, parent, app):
        self.app = app
        self.tree = None
        self.setup_ui(parent)
        self.refresh_table()

    def setup_ui(self, parent):
        """Настройка интерфейса таблицы"""
        # Основной фрейм
        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame,
            text="All DDoS Attacks",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.app.colors["text_light"]
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # Фрейм для таблицы
        table_frame = ctk.CTkFrame(main_frame, fg_color=self.app.colors["card_bg"])
        table_frame.pack(fill="both", expand=True)

        # Создание Treeview
        self.create_treeview(table_frame)

        # Панель управления
        self.create_control_panel(main_frame)

    def create_treeview(self, parent):
        """Создание таблицы"""
        # Создаем стиль для Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background=self.app.colors["card_bg"],
                        foreground=self.app.colors["text_light"],
                        fieldbackground=self.app.colors["card_bg"])
        style.configure("Custom.Treeview.Heading",
                        background=self.app.colors["primary"],
                        foreground=self.app.colors["text_light"],
                        relief="flat")

        # Создаем Treeview
        self.tree = ttk.Treeview(
            parent,
            style="Custom.Treeview",
            columns=("id", "name", "frequency", "danger", "type", "sources", "ports", "targets", "date", "actions"),
            show="headings",
            height=15
        )

        # Настраиваем колонки
        columns_config = [
            ("id", "ID", 80),
            ("name", "Name", 150),
            ("frequency", "Frequency", 100),
            ("danger", "Danger", 100),
            ("type", "Type", 120),
            ("sources", "Source IPs", 150),
            ("ports", "Ports", 120),
            ("targets", "Targets", 100),
            ("date", "Created", 100),
            ("actions", "Actions", 100)
        ]

        for col_id, heading, width in columns_config:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, minwidth=50)

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Упаковка
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Бинд событий
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def create_control_panel(self, parent):
        """Создание панели управления"""
        control_frame = ctk.CTkFrame(parent, fg_color="transparent")
        control_frame.pack(fill="x", pady=(20, 0))

        # Кнопки
        ctk.CTkButton(
            control_frame,
            text="Refresh",
            command=self.refresh_table,
            fg_color=self.app.colors["primary"]
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            control_frame,
            text="Delete Selected",
            command=self.delete_selected,
            fg_color=self.app.colors["danger"]
        ).pack(side="left")

    def on_item_double_click(self, event):
        """Обработка двойного клика по элементу"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            attack_id = self.tree.item(item, "tags")[0]
            self.edit_attack(attack_id)

    def edit_attack(self, attack_id):
        """Редактирование атаки"""
        try:
            attack = self.app.api_client.get_attack(attack_id)
            self.app.current_edit_id = attack_id
            self.app.show_attack_form()

            # Заполняем форму данными атаки
            attack_form = None
            for widget in self.app.content_frame.winfo_children():
                if hasattr(widget, 'fill_form_data'):
                    attack_form = widget
                    break

            if attack_form:
                attack_form.fill_form_data(attack)
        except Exception as e:
            self.show_error(f"Failed to load attack for editing: {e}")

    def delete_selected(self):
        """Удаление выбранной атаки"""
        selection = self.tree.selection()
        if not selection:
            self.show_error("Please select an attack to delete!")
            return

        item = selection[0]
        attack_id = self.tree.item(item, "tags")[0]
        self.delete_attack(attack_id)

    def delete_attack(self, attack_id):
        """Удаление атаки через API"""

        def delete_attack_thread():
            try:
                attack_name = next((a["name"] for a in self.app.attacks if a["id"] == attack_id), "Unknown")
                result = self.app.api_client.delete_attack(attack_id)

                # Обновление UI в основном потоке
                self.app.window.after(0, lambda: self.on_attack_deleted(attack_name))

            except Exception as e:
                self.app.window.after(0, lambda: self.show_error(f"Failed to delete attack: {e}"))

        # Запуск в отдельном потоке
        thread = threading.Thread(target=delete_attack_thread)
        thread.daemon = True
        thread.start()

    def on_attack_deleted(self, attack_name):
        """Обработка успешного удаления атаки"""
        self.app.refresh_attacks()
        self.refresh_table()
        self.show_success(f"Attack '{attack_name}' deleted successfully!")

    def refresh_table(self):
        """Обновление таблицы с данными с сервера"""
        if not self.tree:
            return

        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Безопасно добавляем данные
        for attack in self.app.attacks:
            if not isinstance(attack, dict):
                continue

            # Безопасно извлекаем данные
            attack_id = attack.get("id", "")[:8] + "..."
            name = attack.get("name", "Unknown")
            frequency = attack.get("frequency", "Unknown")
            danger = attack.get("danger", "Unknown")
            attack_type = attack.get("attack_type", "Unknown")

            # Source IPs preview
            source_ips = attack.get("source_ips", [])
            source_ips_preview = ", ".join(source_ips[:2]) + ("..." if len(source_ips) > 2 else "")

            # Ports preview
            ports = attack.get("affected_ports", [])
            ports_preview = ", ".join(map(str, ports[:3])) + ("..." if len(ports) > 3 else "")

            # Targets count
            targets = attack.get("targets", [])
            targets_count = len(targets)

            # Date
            created_date = attack.get("created_at", "Unknown")[:10] if attack.get("created_at") else "Unknown"

            item = self.tree.insert("", "end", values=(
                attack_id,
                name,
                frequency,
                danger,
                attack_type,
                source_ips_preview,
                ports_preview,
                f"{targets_count} targets",
                created_date,
                "Edit/Delete"
            ), tags=(attack.get("id", ""),))

    def show_error(self, message):
        """Показ ошибки"""
        messagebox.showerror("Error", message)

    def show_success(self, message):
        """Показ успеха"""
        messagebox.showinfo("Success", message)