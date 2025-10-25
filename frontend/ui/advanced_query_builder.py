import customtkinter as ctk
from tkinter import ttk
import threading
from api.client import DDOSDatabaseClient


class AdvancedQueryBuilder:
    def __init__(self, parent, app):
        self.app = app
        self.setup_ui(parent)

    def setup_ui(self, parent):
        """Создание интерфейса расширенного построителя запросов"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок
        title_label = ctk.CTkLabel(
            container,
            text="🔍 Advanced Query Builder",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Основной фрейм с вкладками
        main_frame = ctk.CTkFrame(container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        # Левая панель - построитель запросов
        builder_frame = ctk.CTkFrame(main_frame, width=400)
        builder_frame.pack(side="left", fill="y", padx=(0, 10))
        builder_frame.pack_propagate(False)

        # Правая панель - результаты
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.pack(side="right", fill="both", expand=True)

        self.create_query_builder(builder_frame)
        self.create_results_section(results_frame)

    def create_query_builder(self, parent):
        """Создание панели построителя запросов"""
        # Выбор таблиц
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(table_frame, text="Tables:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.table_listbox = ctk.CTkTextbox(table_frame, height=60)
        self.table_listbox.pack(fill="x", pady=5)
        self.table_listbox.insert("1.0", "attacks, targets")

        # Выбор столбцов
        columns_frame = ctk.CTkFrame(parent, fg_color="transparent")
        columns_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(columns_frame, text="Columns (comma separated):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.columns_entry = ctk.CTkEntry(columns_frame, placeholder_text="* or name, frequency, danger")
        self.columns_entry.pack(fill="x", pady=5)

        # Условие WHERE
        where_frame = ctk.CTkFrame(parent, fg_color="transparent")
        where_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(where_frame, text="WHERE Condition:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.where_entry = ctk.CTkEntry(where_frame, placeholder_text="danger = 'high' AND frequency = 'continuous'")
        self.where_entry.pack(fill="x", pady=5)

        # Сортировка ORDER BY
        order_frame = ctk.CTkFrame(parent, fg_color="transparent")
        order_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(order_frame, text="ORDER BY:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        order_subframe = ctk.CTkFrame(order_frame, fg_color="transparent")
        order_subframe.pack(fill="x")

        self.order_field = ctk.CTkEntry(order_subframe, placeholder_text="created_at", width=150)
        self.order_field.pack(side="left", padx=(0, 10))

        self.order_direction = ctk.CTkComboBox(order_subframe, values=["ASC", "DESC"], width=80)
        self.order_direction.pack(side="left")
        self.order_direction.set("DESC")

        # Группировка GROUP BY
        group_frame = ctk.CTkFrame(parent, fg_color="transparent")
        group_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(group_frame, text="GROUP BY:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.group_entry = ctk.CTkEntry(group_frame, placeholder_text="attack_type, danger")
        self.group_entry.pack(fill="x", pady=5)

        # HAVING условие
        having_frame = ctk.CTkFrame(parent, fg_color="transparent")
        having_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(having_frame, text="HAVING:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.having_entry = ctk.CTkEntry(having_frame, placeholder_text="COUNT(*) > 1")
        self.having_entry.pack(fill="x", pady=5)

        # Агрегатные функции
        agg_frame = ctk.CTkFrame(parent, fg_color="transparent")
        agg_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(agg_frame, text="Aggregate Functions:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        agg_subframe = ctk.CTkFrame(agg_frame, fg_color="transparent")
        agg_subframe.pack(fill="x")

        self.agg_function = ctk.CTkComboBox(agg_subframe,
                                            values=["COUNT", "SUM", "AVG", "MIN", "MAX"],
                                            width=100)
        self.agg_function.pack(side="left", padx=(0, 10))
        self.agg_function.set("COUNT")

        self.agg_column = ctk.CTkEntry(agg_subframe, placeholder_text="* or column_name")
        self.agg_column.pack(side="left", fill="x", expand=True)
        self.agg_column.insert(0, "*")

        # Кнопки выполнения
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)

        ctk.CTkButton(
            button_frame,
            text="Build & Execute Query",
            command=self.build_and_execute_query,
            fg_color=self.app.colors["success"]
        ).pack(fill="x", pady=2)

        ctk.CTkButton(
            button_frame,
            text="Generate SQL",
            command=self.generate_sql_only,
            fg_color=self.app.colors["primary"]
        ).pack(fill="x", pady=2)

    def create_results_section(self, parent):
        """Создание панели результатов"""
        # SQL preview
        sql_frame = ctk.CTkFrame(parent, fg_color="transparent")
        sql_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(sql_frame, text="Generated SQL:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.sql_preview = ctk.CTkTextbox(sql_frame, height=80)
        self.sql_preview.pack(fill="x", pady=5)

        # Результаты
        results_label_frame = ctk.CTkFrame(parent, fg_color="transparent")
        results_label_frame.pack(fill="x")

        ctk.CTkLabel(results_label_frame, text="Query Results:", font=ctk.CTkFont(weight="bold")).pack(side="left")

        self.results_count = ctk.CTkLabel(results_label_frame, text="0 rows", text_color=self.app.colors["text_muted"])
        self.results_count.pack(side="right")

        # Таблица результатов
        self.results_tree = ttk.Treeview(parent, show="headings", height=15)

        scrollbar = ctk.CTkScrollbar(parent, orientation="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def build_and_execute_query(self):
        """Построение и выполнение запроса"""
        sql = self.generate_sql_query()
        if sql:
            self.execute_custom_query(sql)

    def generate_sql_only(self):
        """Только генерация SQL без выполнения"""
        sql = self.generate_sql_query()
        if sql:
            self.sql_preview.delete("1.0", "end")
            self.sql_preview.insert("1.0", sql)

    def generate_sql_query(self):
        """Генерация SQL запроса на основе введенных параметров"""
        try:
            # Базовый SELECT
            columns = self.columns_entry.get().strip() or "*"
            sql = f"SELECT {columns}"

            # FROM clause
            tables = self.table_listbox.get("1.0", "end-1c").strip()
            if tables:
                sql += f" FROM {tables}"

            # WHERE clause
            where_condition = self.where_entry.get().strip()
            if where_condition:
                sql += f" WHERE {where_condition}"

            # GROUP BY clause
            group_by = self.group_entry.get().strip()
            if group_by:
                sql += f" GROUP BY {group_by}"

            # HAVING clause
            having_condition = self.having_entry.get().strip()
            if having_condition:
                sql += f" HAVING {having_condition}"

            # ORDER BY clause
            order_field = self.order_field.get().strip()
            if order_field:
                order_dir = self.order_direction.get()
                sql += f" ORDER BY {order_field} {order_dir}"

            return sql

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate SQL: {e}")
            return None

    def execute_custom_query(self, sql):
        """Выполнение пользовательского SQL запроса"""

        def execute_thread():
            try:
                conn = self.app.api_client.db.get_connection()
                cursor = conn.cursor()

                cursor.execute(sql)
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                conn.close()

                # Обновляем UI в основном потоке
                self.app.window.after(0, lambda: self.display_results(columns, results))

            except Exception as e:
                self.app.window.after(0, lambda: messagebox.showerror("Error", f"Query failed: {e}"))

        thread = threading.Thread(target=execute_thread)
        thread.daemon = True
        thread.start()

    def display_results(self, columns, results):
        """Отображение результатов запроса"""
        # Очищаем таблицу
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Настраиваем колонки
        self.results_tree["columns"] = columns
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)

        # Заполняем данными
        for row in results:
            self.results_tree.insert("", "end", values=row)

        # Обновляем счетчик
        self.results_count.configure(text=f"{len(results)} rows")