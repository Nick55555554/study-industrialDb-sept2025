import customtkinter as ctk
from tkinter import ttk
import threading
import re
from api.client import DDOSDatabaseClient


class TextSearchTool:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)

    def setup_ui(self, parent):
        """Создание интерфейса текстового поиска"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок
        title_label = ctk.CTkLabel(
            container,
            text="🔍 Advanced Text Search",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Панель поиска
        search_panel = ctk.CTkFrame(container, fg_color=self.app.colors["card_bg"], corner_radius=12)
        search_panel.pack(fill="x", pady=(0, 15))

        search_content = ctk.CTkFrame(search_panel, fg_color="transparent")
        search_content.pack(fill="x", padx=20, pady=15)

        # Первая строка - таблица и столбец
        row1 = ctk.CTkFrame(search_content, fg_color="transparent")
        row1.pack(fill="x", pady=5)

        ctk.CTkLabel(row1, text="Table:").pack(side="left")
        self.search_table = ctk.CTkComboBox(row1, values=["attacks", "targets"], width=120)
        self.search_table.pack(side="left", padx=(10, 20))
        self.search_table.set("attacks")

        ctk.CTkLabel(row1, text="Column:").pack(side="left")
        self.search_column = ctk.CTkComboBox(row1, values=["name", "attack_type", "frequency", "danger"], width=120)
        self.search_column.pack(side="left", padx=(10, 20))
        self.search_column.set("name")

        # Вторая строка - поисковый запрос и тип поиска
        row2 = ctk.CTkFrame(search_content, fg_color="transparent")
        row2.pack(fill="x", pady=5)

        ctk.CTkLabel(row2, text="Search For:").pack(side="left")
        self.search_pattern = ctk.CTkEntry(row2, placeholder_text="Enter search pattern...")
        self.search_pattern.pack(side="left", padx=(10, 20), fill="x", expand=True)

        ctk.CTkLabel(row2, text="Search Type:").pack(side="left")
        self.search_type = ctk.CTkComboBox(row2, values=[
            "LIKE (Case Sensitive)",
            "ILIKE (Case Insensitive)",
            "POSIX Regex (~)",
            "POSIX Regex Case Insensitive (~*)",
            "POSIX Regex Not Match (!~)",
            "POSIX Regex Not Match Case Insensitive (!~*)"
        ], width=200)
        self.search_type.pack(side="left", padx=(10, 0))
        self.search_type.set("LIKE (Case Sensitive)")

        # Третья строка - кнопки
        row3 = ctk.CTkFrame(search_content, fg_color="transparent")
        row3.pack(fill="x", pady=5)

        ctk.CTkButton(
            row3,
            text="Search",
            command=self.execute_search,
            fg_color=self.app.colors["primary"],
            width=100
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            row3,
            text="Clear",
            command=self.clear_search,
            width=80
        ).pack(side="left")

        # Справка по регулярным выражениям
        help_btn = ctk.CTkButton(
            row3,
            text="Regex Help",
            command=self.show_regex_help,
            width=80,
            fg_color=self.app.colors["warning"]
        )
        help_btn.pack(side="right")

        # Результаты поиска
        results_frame = ctk.CTkFrame(container)
        results_frame.pack(fill="both", expand=True)

        # Заголовок результатов
        results_header = ctk.CTkFrame(results_frame, fg_color="transparent")
        results_header.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(results_header, text="Search Results",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

        self.results_count = ctk.CTkLabel(results_header, text="0 matches found",
                                          text_color=self.app.colors["text_muted"])
        self.results_count.pack(side="right")

        # Таблица результатов
        self.results_tree = ttk.Treeview(results_frame, show="headings", height=15)

        scrollbar = ctk.CTkScrollbar(results_frame, orientation="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))

    def execute_search(self):
        """Выполнение поиска"""
        pattern = self.search_pattern.get().strip()
        if not pattern:
            messagebox.showwarning("Warning", "Please enter search pattern")
            return

        table = self.search_table.get()
        column = self.search_column.get()
        search_type = self.search_type.get()

        def search_thread():
            try:
                conn = self.app.api_client.db.get_connection()
                cursor = conn.cursor()

                # Формируем SQL в зависимости от типа поиска
                if search_type == "LIKE (Case Sensitive)":
                    sql = f"SELECT * FROM {table} WHERE {column} LIKE %s"
                    params = [f"%{pattern}%"]
                elif search_type == "ILIKE (Case Insensitive)":
                    sql = f"SELECT * FROM {table} WHERE {column} ILIKE %s"
                    params = [f"%{pattern}%"]
                elif search_type == "POSIX Regex (~)":
                    sql = f"SELECT * FROM {table} WHERE {column} ~ %s"
                    params = [pattern]
                elif search_type == "POSIX Regex Case Insensitive (~*)":
                    sql = f"SELECT * FROM {table} WHERE {column} ~* %s"
                    params = [pattern]
                elif search_type == "POSIX Regex Not Match (!~)":
                    sql = f"SELECT * FROM {table} WHERE {column} !~ %s"
                    params = [pattern]
                elif search_type == "POSIX Regex Not Match Case Insensitive (!~*)":
                    sql = f"SELECT * FROM {table} WHERE {column} !~* %s"
                    params = [pattern]

                cursor.execute(sql, params)
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                conn.close()

                # Обновляем UI
                self.app.window.after(0, lambda: self.display_search_results(columns, results, pattern))

            except Exception as e:
                self.app.window.after(0, lambda: messagebox.showerror("Error", f"Search failed: {e}"))

        thread = threading.Thread(target=search_thread)
        thread.daemon = True
        thread.start()

    def display_search_results(self, columns, results, pattern):
        """Отображение результатов поиска"""
        # Очищаем таблицу
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Настраиваем колонки
        self.results_tree["columns"] = columns
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120)

        # Заполняем данными с подсветкой совпадений
        for row in results:
            self.results_tree.insert("", "end", values=row)

        # Обновляем счетчик
        self.results_count.configure(text=f"{len(results)} matches found for '{pattern}'")

    def clear_search(self):
        """Очистка результатов поиска"""
        self.search_pattern.delete(0, "end")
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results_count.configure(text="0 matches found")

    def show_regex_help(self):
        """Показ справки по регулярным выражениям"""
        help_text = """
📖 PostgreSQL Regular Expressions Help:

Basic Patterns:
• .       - Any single character
• .*      - Any characters (wildcard)
• ^       - Start of string
• $       - End of string
• [abc]   - Any of a, b, or c
• [^abc]  - Any character except a, b, or c
• [a-z]   - Any lowercase letter
• [A-Z]   - Any uppercase letter
• [0-9]   - Any digit

Quantifiers:
• *       - 0 or more
• +       - 1 or more  
• ?       - 0 or 1
• {n}     - Exactly n
• {n,}    - n or more
• {n,m}   - Between n and m

Character Classes:
• \\d     - Digit
• \\D     - Non-digit
• \\w     - Word character
• \\W     - Non-word character
• \\s     - Whitespace
• \\S     - Non-whitespace

Examples:
• '^DDoS'    - Starts with "DDoS"
• 'attack$'  - Ends with "attack"
• 'high|low' - Contains "high" or "low"
• '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}' - IP address pattern
        """

        # Создаем модальное окно со справкой
        help_window = ctk.CTkToplevel(self.app.window)
        help_window.title("Regex Help")
        help_window.geometry("500x400")
        help_window.resizable(False, False)

        # Центрируем окно
        help_window.transient(self.app.window)
        help_window.grab_set()

        text_widget = ctk.CTkTextbox(help_window, wrap="word")
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", help_text)
        text_widget.configure(state="disabled")

        ctk.CTkButton(
            help_window,
            text="Close",
            command=help_window.destroy
        ).pack(pady=(0, 20))