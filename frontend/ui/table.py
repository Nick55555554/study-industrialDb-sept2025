import customtkinter as ctk
from tkinter import ttk, messagebox
import threading
import re

class AttackTable:
    def __init__(self, parent, app):
        self.app = app
        self.selected_columns = []
        self.setup_ui(parent)

    def setup_ui(self, parent):
        """Создание интерфейса конструктора запросов"""
        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Заголовок
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(header_frame, text="🔍 Advanced Query Builder", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")

        # Основной контейнер с вкладками
        self.tabview = ctk.CTkTabview(main_frame, fg_color=self.app.colors["card_bg"])
        self.tabview.pack(fill="both", expand=True)

        # Создаем вкладки
        self.select_tab = self.tabview.add("📋 SELECT Builder")
        self.search_tab = self.tabview.add("🔎 Text Search")
        self.functions_tab = self.tabview.add("🛠️ String Functions")

        # Наполняем вкладки
        self.setup_select_tab()
        self.setup_search_tab()
        self.setup_functions_tab()

        # Статус бар
        self.status_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=30)
        self.status_frame.pack(fill="x", pady=(10, 0))
        self.status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready to build queries",
                                         text_color=self.app.colors["text_muted"],
                                         font=ctk.CTkFont(size=12))
        self.status_label.pack(side="left")

    def setup_select_tab(self):
        """Вкладка конструктора SELECT запросов"""
        container = ctk.CTkFrame(self.select_tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Верхняя панель - выбор таблицы
        top_panel = ctk.CTkFrame(container, fg_color=self.app.colors["card_bg"], corner_radius=12)
        top_panel.pack(fill="x", pady=(0, 10))

        top_content = ctk.CTkFrame(top_panel, fg_color="transparent")
        top_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(top_content, text="Select Table:", 
                    font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))

        self.table_selector = ctk.CTkComboBox(top_content, 
                                             values=["Loading..."],
                                             width=200,
                                             command=self.on_table_selected)
        self.table_selector.pack(side="left", padx=(0, 10))

        ctk.CTkButton(top_content, text="🔄 Refresh", 
                     command=self.refresh_table_structure,
                     width=80).pack(side="left")

        # Основной контент
        main_content = ctk.CTkFrame(container, fg_color="transparent")
        main_content.pack(fill="both", expand=True)

        # Левая панель - выбор колонок и условия
        left_panel = ctk.CTkFrame(main_content, fg_color=self.app.colors["card_bg"], corner_radius=12)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Секция выбора колонок
        columns_section = ctk.CTkFrame(left_panel, fg_color="transparent")
        columns_section.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(columns_section, text="📊 Select Columns", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

        # Список доступных колонок
        columns_frame = ctk.CTkFrame(columns_section, fg_color="transparent")
        columns_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(columns_frame, text="Available Columns:").pack(anchor="w")
        
        self.available_columns_list = tk.Listbox(columns_frame, 
                                               bg=self.app.colors["card_bg"],
                                               fg=self.app.colors["text_light"],
                                               selectbackground=self.app.colors["primary"],
                                               height=6)
        scrollbar1 = ctk.CTkScrollbar(columns_frame, orientation="vertical", command=self.available_columns_list.yview)
        self.available_columns_list.configure(yscrollcommand=scrollbar1.set)
        
        self.available_columns_list.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="right", fill="y")

        # Кнопки управления выбором колонок
        column_buttons = ctk.CTkFrame(columns_frame, fg_color="transparent")
        column_buttons.pack(fill="x", pady=5)

        ctk.CTkButton(column_buttons, text="➡️ Add", 
                     command=self.add_column,
                     width=80).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(column_buttons, text="⬅️ Remove", 
                     command=self.remove_column,
                     width=80).pack(side="left", padx=5)

        ctk.CTkButton(column_buttons, text="⭐ Add All", 
                     command=self.add_all_columns,
                     width=80).pack(side="left", padx=5)

        # Выбранные колонки
        ctk.CTkLabel(columns_frame, text="Selected Columns:").pack(anchor="w", pady=(10, 0))
        
        self.selected_columns_list = tk.Listbox(columns_frame,
                                              bg=self.app.colors["card_bg"],
                                              fg=self.app.colors["text_light"],
                                              selectbackground=self.app.colors["success"],
                                              height=6)
        scrollbar2 = ctk.CTkScrollbar(columns_frame, orientation="vertical", command=self.selected_columns_list.yview)
        self.selected_columns_list.configure(yscrollcommand=scrollbar2.set)
        
        self.selected_columns_list.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")

        # Секция WHERE условия
        where_section = ctk.CTkFrame(left_panel, fg_color="transparent")
        where_section.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(where_section, text="🔍 WHERE Conditions", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

        where_content = ctk.CTkFrame(where_section, fg_color="transparent")
        where_content.pack(fill="x", pady=10)

        # Поле для WHERE условия
        ctk.CTkLabel(where_content, text="WHERE Condition:").pack(anchor="w")
        self.where_condition = ctk.CTkEntry(where_content, 
                                          placeholder_text="age > 18 AND name LIKE 'A%'")
        self.where_condition.pack(fill="x", pady=(5, 10))

        # Секция GROUP BY и HAVING
        group_section = ctk.CTkFrame(left_panel, fg_color="transparent")
        group_section.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(group_section, text="📊 GROUP BY & HAVING", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

        group_content = ctk.CTkFrame(group_section, fg_color="transparent")
        group_content.pack(fill="x", pady=10)

        ctk.CTkLabel(group_content, text="GROUP BY Columns:").pack(anchor="w")
        self.group_by_columns = ctk.CTkEntry(group_content, 
                                           placeholder_text="department, year")
        self.group_by_columns.pack(fill="x", pady=(5, 5))

        ctk.CTkLabel(group_content, text="HAVING Condition:").pack(anchor="w", pady=(10, 0))
        self.having_condition = ctk.CTkEntry(group_content, 
                                           placeholder_text="COUNT(*) > 5")
        self.having_condition.pack(fill="x", pady=(5, 10))

        # Правая панель - ORDER BY и выполнение
        right_panel = ctk.CTkFrame(main_content, fg_color=self.app.colors["card_bg"], corner_radius=12)
        right_panel.pack(side="left", fill="both", expand=True)

        # Секция ORDER BY
        order_section = ctk.CTkFrame(right_panel, fg_color="transparent")
        order_section.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(order_section, text="📈 ORDER BY", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

        order_content = ctk.CTkFrame(order_section, fg_color="transparent")
        order_content.pack(fill="x", pady=10)

        ctk.CTkLabel(order_content, text="Sort Columns:").pack(anchor="w")
        self.order_by_columns = ctk.CTkEntry(order_content, 
                                           placeholder_text="name ASC, age DESC")
        self.order_by_columns.pack(fill="x", pady=(5, 10))

        # Секция агрегатных функций
        aggregate_section = ctk.CTkFrame(right_panel, fg_color="transparent")
        aggregate_section.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(aggregate_section, text="🧮 Aggregate Functions", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

        aggregate_content = ctk.CTkFrame(aggregate_section, fg_color="transparent")
        aggregate_content.pack(fill="x", pady=10)

        # Кнопки быстрого добавления агрегатных функций
        agg_buttons_frame = ctk.CTkFrame(aggregate_content, fg_color="transparent")
        agg_buttons_frame.pack(fill="x")

        ctk.CTkButton(agg_buttons_frame, text="COUNT(*)", 
                     command=lambda: self.add_aggregate("COUNT(*)"),
                     width=100).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(agg_buttons_frame, text="AVG(column)", 
                     command=lambda: self.show_aggregate_dialog("AVG"),
                     width=100).pack(side="left", padx=5)
        
        ctk.CTkButton(agg_buttons_frame, text="SUM(column)", 
                     command=lambda: self.show_aggregate_dialog("SUM"),
                     width=100).pack(side="left", padx=5)

        agg_buttons_frame2 = ctk.CTkFrame(aggregate_content, fg_color="transparent")
        agg_buttons_frame2.pack(fill="x", pady=5)

        ctk.CTkButton(agg_buttons_frame2, text="MAX(column)", 
                     command=lambda: self.show_aggregate_dialog("MAX"),
                     width=100).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(agg_buttons_frame2, text="MIN(column)", 
                     command=lambda: self.show_aggregate_dialog("MIN"),
                     width=100).pack(side="left", padx=5)

        # Секция предварительного просмотра SQL
        preview_section = ctk.CTkFrame(right_panel, fg_color="transparent")
        preview_section.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(preview_section, text="👁️ SQL Preview", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

        self.sql_preview = ctk.CTkTextbox(preview_section, height=120)
        self.sql_preview.pack(fill="both", expand=True, pady=(10, 10))
        self.sql_preview.configure(state="disabled")

        # Кнопки выполнения
        action_buttons = ctk.CTkFrame(right_panel, fg_color="transparent")
        action_buttons.pack(fill="x", padx=20, pady=15)

        ctk.CTkButton(action_buttons, text="🔄 Update Preview", 
                     command=self.update_sql_preview,
                     width=140).pack(side="left", padx=(0, 10))

        ctk.CTkButton(action_buttons, text="⚡ Execute Query", 
                     command=self.execute_query,
                     fg_color=self.app.colors["success"],
                     hover_color="#1a8a4f",
                     width=140).pack(side="left")

    def setup_search_tab(self):
        """Вкладка текстового поиска"""
        container = ctk.CTkFrame(self.search_tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Верхняя панель - выбор таблицы и колонки
        top_panel = ctk.CTkFrame(container, fg_color=self.app.colors["card_bg"], corner_radius=12)
        top_panel.pack(fill="x", pady=(0, 10))

        top_content = ctk.CTkFrame(top_panel, fg_color="transparent")
        top_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(top_content, text="Select Table & Column:", 
                    font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))

        self.search_table_selector = ctk.CTkComboBox(top_content, 
                                                   values=["Loading..."],
                                                   width=150,
                                                   command=self.on_search_table_selected)
        self.search_table_selector.pack(side="left", padx=(0, 10))

        self.search_column_selector = ctk.CTkComboBox(top_content, 
                                                    values=["Select table first"],
                                                    width=150)
        self.search_column_selector.pack(side="left", padx=(0, 10))

        # Основной контент
        main_content = ctk.CTkFrame(container, fg_color="transparent")
        main_content.pack(fill="both", expand=True)

        # Левая панель - настройки поиска
        left_panel = ctk.CTkFrame(main_content, fg_color=self.app.colors["card_bg"], corner_radius=12)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        search_config_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        search_config_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(search_config_frame, text="🔍 Search Configuration", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 15))

        # Тип поиска
        ctk.CTkLabel(search_config_frame, text="Search Type:").pack(anchor="w")
        self.search_type = ctk.CTkComboBox(search_config_frame,
                                         values=["LIKE Pattern", "POSIX Regex", "Full Text Search"])
        self.search_type.pack(fill="x", pady=(5, 15))
        self.search_type.set("LIKE Pattern")
        self.search_type.configure(command=self.on_search_type_changed)

        # Поле поиска
        ctk.CTkLabel(search_config_frame, text="Search Pattern:").pack(anchor="w")
        self.search_pattern = ctk.CTkEntry(search_config_frame, 
                                         placeholder_text="Enter search pattern")
        self.search_pattern.pack(fill="x", pady=(5, 10))

        # Опции для LIKE
        self.like_options_frame = ctk.CTkFrame(search_config_frame, fg_color="transparent")
        self.like_options_frame.pack(fill="x", pady=5)

        self.case_sensitive = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.like_options_frame, text="Case Sensitive", 
                       variable=self.case_sensitive).pack(anchor="w")

        # Опции для Regex
        self.regex_options_frame = ctk.CTkFrame(search_config_frame, fg_color="transparent")
        
        self.regex_flags = ctk.StringVar(value="")
        ctk.CTkCheckBox(self.regex_options_frame, text="Case Insensitive (i)",
                       variable=ctk.BooleanVar(value=False),
                       command=lambda: self.toggle_regex_flag('i')).pack(anchor="w")
        ctk.CTkCheckBox(self.regex_options_frame, text="Multiline (m)",
                       variable=ctk.BooleanVar(value=False),
                       command=lambda: self.toggle_regex_flag('m')).pack(anchor="w")

        # Примеры поиска
        examples_frame = ctk.CTkFrame(search_config_frame, fg_color="transparent")
        examples_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(examples_frame, text="💡 Search Examples:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        examples_text = """
LIKE Examples:
• 'john%' - names starting with 'john'
• '%son' - names ending with 'son'  
• '%smith%' - names containing 'smith'
• '_e%' - names with 'e' as second letter

Regex Examples:
• '^J.*n$' - starts with J, ends with n
• 'Sm(th|ith)' - Smith or Sm ith
• '[A-Z][a-z]+' - Capitalized words
• '\\d{3}-\\d{2}-\\d{4}' - SSN pattern
        """
        
        examples_label = ctk.CTkLabel(examples_frame, text=examples_text,
                                    justify="left", font=ctk.CTkFont(size=11),
                                    text_color=self.app.colors["text_muted"])
        examples_label.pack(anchor="w", pady=5)

        # Кнопки поиска
        search_buttons = ctk.CTkFrame(search_config_frame, fg_color="transparent")
        search_buttons.pack(fill="x", pady=10)

        ctk.CTkButton(search_buttons, text="🔍 Test Pattern", 
                     command=self.test_search_pattern,
                     width=120).pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_buttons, text="⚡ Execute Search", 
                     command=self.execute_search,
                     fg_color=self.app.colors["primary"],
                     hover_color="#1f4a63",
                     width=120).pack(side="left")

        # Правая панель - результаты тестирования
        right_panel = ctk.CTkFrame(main_content, fg_color=self.app.colors["card_bg"], corner_radius=12)
        right_panel.pack(side="left", fill="both", expand=True)

        results_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(results_frame, text="🧪 Pattern Testing", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 15))

        # Поле для тестовых данных
        ctk.CTkLabel(results_frame, text="Test Data (one per line):").pack(anchor="w")
        self.test_data = ctk.CTkTextbox(results_frame, height=100)
        self.test_data.pack(fill="x", pady=(5, 10))
        self.test_data.insert("1.0", "John Smith\nJane Doe\nBob Johnson\nAlice Williams")

        # Результаты тестирования
        ctk.CTkLabel(results_frame, text="Test Results:").pack(anchor="w")
        self.test_results = ctk.CTkTextbox(results_frame, height=150)
        self.test_results.pack(fill="both", expand=True, pady=(5, 10))
        self.test_results.configure(state="disabled")

    def setup_functions_tab(self):
        """Вкладка функций работы со строками"""
        container = ctk.CTkFrame(self.functions_tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Верхняя панель - ввод данных
        top_panel = ctk.CTkFrame(container, fg_color=self.app.colors["card_bg"], corner_radius=12)
        top_panel.pack(fill="x", pady=(0, 10))

        top_content = ctk.CTkFrame(top_panel, fg_color="transparent")
        top_content.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(top_content, text="Input String:", 
                    font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))

        self.input_string = ctk.CTkEntry(top_content, 
                                       placeholder_text="Enter text to process...",
                                       width=300)
        self.input_string.pack(side="left", padx=(0, 10))
        self.input_string.insert(0, "  Hello World  ")

        ctk.CTkButton(top_content, text="🔄 Process", 
                     command=self.process_string_functions,
                     width=100).pack(side="left")

        # Основной контент - функции
        main_content = ctk.CTkFrame(container, fg_color="transparent")
        main_content.pack(fill="both", expand=True)

        # Левая панель - базовые функции
        left_panel = ctk.CTkFrame(main_content, fg_color=self.app.colors["card_bg"], corner_radius=12)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        basic_functions_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        basic_functions_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(basic_functions_frame, text="🛠️ Basic String Functions", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 15))

        # Кнопки базовых функций
        basic_buttons1 = ctk.CTkFrame(basic_functions_frame, fg_color="transparent")
        basic_buttons1.pack(fill="x", pady=5)

        ctk.CTkButton(basic_buttons1, text="UPPER()", 
                     command=lambda: self.apply_string_function("UPPER"),
                     width=120).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(basic_buttons1, text="LOWER()", 
                     command=lambda: self.apply_string_function("LOWER"),
                     width=120).pack(side="left", padx=5)

        basic_buttons2 = ctk.CTkFrame(basic_functions_frame, fg_color="transparent")
        basic_buttons2.pack(fill="x", pady=5)

        ctk.CTkButton(basic_buttons2, text="TRIM()", 
                     command=lambda: self.apply_string_function("TRIM"),
                     width=120).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(basic_buttons2, text="LTRIM()", 
                     command=lambda: self.apply_string_function("LTRIM"),
                     width=120).pack(side="left", padx=5)

        basic_buttons3 = ctk.CTkFrame(basic_functions_frame, fg_color="transparent")
        basic_buttons3.pack(fill="x", pady=5)

        ctk.CTkButton(basic_buttons3, text="RTRIM()", 
                     command=lambda: self.apply_string_function("RTRIM"),
                     width=120).pack(side="left", padx=(0, 5))

        # Функции подстрок
        substring_frame = ctk.CTkFrame(basic_functions_frame, fg_color="transparent")
        substring_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(substring_frame, text="Substring Functions:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        substring_buttons = ctk.CTkFrame(substring_frame, fg_color="transparent")
        substring_buttons.pack(fill="x", pady=5)

        ctk.CTkButton(substring_buttons, text="SUBSTRING()", 
                     command=self.show_substring_dialog,
                     width=120).pack(side="left", padx=(0, 5))

        # Правая панель - продвинутые функции
        right_panel = ctk.CTkFrame(main_content, fg_color=self.app.colors["card_bg"], corner_radius=12)
        right_panel.pack(side="left", fill="both", expand=True)

        advanced_functions_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        advanced_functions_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(advanced_functions_frame, text="⚡ Advanced String Functions", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0, 15))

        # Функции дополнения
        padding_frame = ctk.CTkFrame(advanced_functions_frame, fg_color="transparent")
        padding_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(padding_frame, text="Padding Functions:").pack(anchor="w")

        padding_buttons = ctk.CTkFrame(padding_frame, fg_color="transparent")
        padding_buttons.pack(fill="x", pady=5)

        ctk.CTkButton(padding_buttons, text="LPAD()", 
                     command=self.show_lpad_dialog,
                     width=120).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(padding_buttons, text="RPAD()", 
                     command=self.show_rpad_dialog,
                     width=120).pack(side="left", padx=5)

        # Конкатенация
        concat_frame = ctk.CTkFrame(advanced_functions_frame, fg_color="transparent")
        concat_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(concat_frame, text="Concatenation:").pack(anchor="w")

        concat_content = ctk.CTkFrame(concat_frame, fg_color="transparent")
        concat_content.pack(fill="x", pady=5)

        ctk.CTkLabel(concat_content, text="String 2:").pack(side="left", padx=(0, 5))
        self.concat_string = ctk.CTkEntry(concat_content, 
                                        placeholder_text="Text to concatenate",
                                        width=150)
        self.concat_string.pack(side="left", padx=(0, 10))

        ctk.CTkButton(concat_content, text="CONCAT", 
                     command=self.apply_concat,
                     width=100).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(concat_content, text="||", 
                     command=self.apply_concat_operator,
                     width=50).pack(side="left")

        # Результаты
        results_frame = ctk.CTkFrame(advanced_functions_frame, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, pady=15)

        ctk.CTkLabel(results_frame, text="📊 Results:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        self.function_results = ctk.CTkTextbox(results_frame, height=150)
        self.function_results.pack(fill="both", expand=True, pady=(5, 0))
        self.function_results.configure(state="disabled")

    def on_search_type_changed(self, choice):
        """Обновление интерфейса при изменении типа поиска"""
        search_type = self.search_type.get()
        
        # Скрываем все опции
        self.like_options_frame.pack_forget()
        self.regex_options_frame.pack_forget()
        
        # Показываем соответствующие опции
        if search_type == "LIKE Pattern":
            self.like_options_frame.pack(fill="x", pady=5)
        elif search_type == "POSIX Regex":
            self.regex_options_frame.pack(fill="x", pady=5)

    def toggle_regex_flag(self, flag):
        """Переключение флагов regex"""
        # Реализация переключения флагов
        pass

    def on_table_selected(self, choice):
        """Обработка выбора таблицы"""
        self.refresh_columns_list()

    def on_search_table_selected(self, choice):
        """Обработка выбора таблицы для поиска"""
        self.refresh_search_columns()

    def refresh_table_structure(self):
        """Обновление структуры таблицы"""
        self.status_label.configure(text="🔄 Loading table structure...")
        
        def refresh_thread():
            try:
                # Здесь будет вызов API для получения структуры таблицы
                tables = ["attacks", "users", "logs", "settings"]
                columns = ["id", "name", "description", "created_at", "status"]
                
                self.app.window.after(0, lambda: self.on_table_structure_loaded(tables, columns))
            except Exception as e:
                self.app.window.after(0, lambda: self.show_error(f"Failed to load table structure: {e}"))

        thread = threading.Thread(target=refresh_thread)
        thread.daemon = True
        thread.start()

    def on_table_structure_loaded(self, tables, columns):
        """Обработка загруженной структуры таблицы"""
        # Обновляем селекторы таблиц
        self.table_selector.configure(values=tables)
        self.search_table_selector.configure(values=tables)
        
        if tables:
            self.table_selector.set(tables[0])
            self.search_table_selector.set(tables[0])
        
        # Обновляем список колонок
        self.available_columns_list.delete(0, tk.END)
        for column in columns:
            self.available_columns_list.insert(tk.END, column)
        
        self.status_label.configure(text=f"✅ Loaded {len(columns)} columns")

    def refresh_columns_list(self):
        """Обновление списка колонок для выбранной таблицы"""
        table_name = self.table_selector.get()
        if not table_name or table_name == "Loading...":
            return

        # Здесь будет вызов API для получения колонок таблицы
        # Временные данные для демонстрации
        columns = ["id", "name", "description", "created_at", "status", "severity"]
        
        self.available_columns_list.delete(0, tk.END)
        for column in columns:
            self.available_columns_list.insert(tk.END, column)

    def refresh_search_columns(self):
        """Обновление колонок для поиска"""
        table_name = self.search_table_selector.get()
        if not table_name or table_name == "Loading...":
            return

        # Здесь будет вызов API для получения колонок таблицы
        columns = ["name", "description", "notes", "title"]
        
        self.search_column_selector.configure(values=columns)
        if columns:
            self.search_column_selector.set(columns[0])

    def add_column(self):
        """Добавление выбранной колонки"""
        selection = self.available_columns_list.curselection()
        if not selection:
            return

        column_name = self.available_columns_list.get(selection[0])
        if column_name not in self.selected_columns:
            self.selected_columns.append(column_name)
            self.selected_columns_list.insert(tk.END, column_name)

    def remove_column(self):
        """Удаление выбранной колонки"""
        selection = self.selected_columns_list.curselection()
        if not selection:
            return

        column_name = self.selected_columns_list.get(selection[0])
        if column_name in self.selected_columns:
            self.selected_columns.remove(column_name)
            self.selected_columns_list.delete(selection[0])

    def add_all_columns(self):
        """Добавление всех колонок"""
        all_columns = self.available_columns_list.get(0, tk.END)
        self.selected_columns.clear()
        self.selected_columns_list.delete(0, tk.END)
        
        for column in all_columns:
            self.selected_columns.append(column)
            self.selected_columns_list.insert(tk.END, column)

    def add_aggregate(self, aggregate_func):
        """Добавление агрегатной функции"""
        if aggregate_func == "COUNT(*)":
            self.selected_columns.append("COUNT(*)")
            self.selected_columns_list.insert(tk.END, "COUNT(*)")

    def show_aggregate_dialog(self, func_name):
        """Показ диалога для агрегатной функции с колонкой"""
        dialog = ctk.CTkToplevel(self.app.window)
        dialog.title(f"{func_name} Function")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.app.window)
        dialog.grab_set()

        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(content, text=f"Select column for {func_name}:").pack(anchor="w", pady=(0, 10))
        
        column_combo = ctk.CTkComboBox(content, values=list(self.available_columns_list.get(0, tk.END)))
        column_combo.pack(fill="x", pady=(0, 15))

        def add_aggregate_column():
            column = column_combo.get()
            if column:
                agg_func = f"{func_name}({column})"
                self.selected_columns.append(agg_func)
                self.selected_columns_list.insert(tk.END, agg_func)
                dialog.destroy()

        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x")

        ctk.CTkButton(buttons_frame, text="Add", 
                     command=add_aggregate_column).pack(side="right", padx=(10, 0))

        ctk.CTkButton(buttons_frame, text="Cancel", 
                     command=dialog.destroy).pack(side="right")

    def update_sql_preview(self):
        """Обновление предварительного просмотра SQL"""
        try:
            # Формируем базовый SELECT
            if not self.selected_columns:
                columns = "*"
            else:
                columns = ", ".join(self.selected_columns)
            
            table_name = self.table_selector.get()
            sql = f"SELECT {columns}\nFROM {table_name}"

            # Добавляем WHERE
            where_condition = self.where_condition.get().strip()
            if where_condition:
                sql += f"\nWHERE {where_condition}"

            # Добавляем GROUP BY
            group_by = self.group_by_columns.get().strip()
            if group_by:
                sql += f"\nGROUP BY {group_by}"

                # Добавляем HAVING
                having_condition = self.having_condition.get().strip()
                if having_condition:
                    sql += f"\nHAVING {having_condition}"

            # Добавляем ORDER BY
            order_by = self.order_by_columns.get().strip()
            if order_by:
                sql += f"\nORDER BY {order_by}"

            # Обновляем preview
            self.sql_preview.configure(state="normal")
            self.sql_preview.delete("1.0", "end")
            self.sql_preview.insert("1.0", sql)
            self.sql_preview.configure(state="disabled")

        except Exception as e:
            self.show_error(f"Error generating SQL: {e}")

    def execute_query(self):
        """Выполнение сформированного запроса"""
        sql = self.sql_preview.get("1.0", "end-1c").strip()
        if not sql:
            self.show_error("No query to execute!")
            return

        self.status_label.configure(text="⚡ Executing query...")
        
        def execute_thread():
            try:
                # Здесь будет вызов API для выполнения запроса
                # Временная заглушка
                self.app.window.after(0, lambda: self.on_query_executed([
                    {"id": 1, "name": "Example", "count": 5},
                    {"id": 2, "name": "Test", "count": 3}
                ]))
            except Exception as e:
                self.app.window.after(0, lambda: self.show_error(f"Query execution failed: {e}"))

        thread = threading.Thread(target=execute_thread)
        thread.daemon = True
        thread.start()

    def on_query_executed(self, results):
        """Обработка результатов выполнения запроса"""
        self.status_label.configure(text=f"✅ Query executed - {len(results)} rows")
        # Здесь будет отображение результатов в основном интерфейсе
        self.app.show_success(f"Query executed successfully! Found {len(results)} rows.")

    def test_search_pattern(self):
        """Тестирование поискового шаблона"""
        pattern = self.search_pattern.get().strip()
        test_data = self.test_data.get("1.0", "end-1c").strip()
        
        if not pattern:
            self.show_error("Please enter a search pattern!")
            return

        if not test_data:
            self.show_error("Please enter test data!")
            return

        search_type = self.search_type.get()
        test_lines = test_data.split('\n')
        results = []

        try:
            if search_type == "LIKE Pattern":
                # Преобразуем LIKE в regex для тестирования
                regex_pattern = pattern.replace('%', '.*').replace('_', '.')
                if not self.case_sensitive.get():
                    regex_pattern = f"(?i){regex_pattern}"
                
                for line in test_lines:
                    if line and re.match(regex_pattern, line):
                        results.append(f"✓ MATCH: {line}")
                    else:
                        results.append(f"✗ NO MATCH: {line}")

            elif search_type == "POSIX Regex":
                flags = re.IGNORECASE if not self.case_sensitive.get() else 0
                for line in test_lines:
                    if line and re.search(pattern, line, flags):
                        results.append(f"✓ MATCH: {line}")
                    else:
                        results.append(f"✗ NO MATCH: {line}")

            # Обновляем результаты
            self.test_results.configure(state="normal")
            self.test_results.delete("1.0", "end")
            self.test_results.insert("1.0", "\n".join(results))
            self.test_results.configure(state="disabled")

        except re.error as e:
            self.show_error(f"Invalid regex pattern: {e}")

    def execute_search(self):
        """Выполнение поискового запроса"""
        table_name = self.search_table_selector.get()
        column_name = self.search_column_selector.get()
        pattern = self.search_pattern.get().strip()
        search_type = self.search_type.get()

        if not all([table_name, column_name, pattern]):
            self.show_error("Please fill all search fields!")
            return

        self.status_label.configure(text="🔍 Executing search...")
        
        def search_thread():
            try:
                # Здесь будет вызов API для выполнения поиска
                # Временная заглушка
                results = [{"id": 1, column_name: "Example match"}]
                self.app.window.after(0, lambda: self.on_search_executed(results))
            except Exception as e:
                self.app.window.after(0, lambda: self.show_error(f"Search failed: {e}"))

        thread = threading.Thread(target=search_thread)
        thread.daemon = True
        thread.start()

    def on_search_executed(self, results):
        """Обработка результатов поиска"""
        self.status_label.configure(text=f"✅ Search completed - {len(results)} matches")
        self.app.show_success(f"Search completed! Found {len(results)} matches.")

    def process_string_functions(self):
        """Обработка строковых функций"""
        input_text = self.input_string.get().strip()
        if not input_text:
            self.show_error("Please enter input text!")
            return

        # Очищаем предыдущие результаты
        self.function_results.configure(state="normal")
        self.function_results.delete("1.0", "end")
        
        # Добавляем заголовок
        self.function_results.insert("end", f"Input: '{input_text}'\n")
        self.function_results.insert("end", "="*50 + "\n\n")
        
        self.function_results.configure(state="disabled")

    def apply_string_function(self, func_name):
        """Применение строковой функции"""
        input_text = self.input_string.get().strip()
        if not input_text:
            self.show_error("Please enter input text!")
            return

        result = ""
        
        if func_name == "UPPER":
            result = input_text.upper()
        elif func_name == "LOWER":
            result = input_text.lower()
        elif func_name == "TRIM":
            result = input_text.strip()
        elif func_name == "LTRIM":
            result = input_text.lstrip()
        elif func_name == "RTRIM":
            result = input_text.rstrip()

        self.display_function_result(func_name, input_text, result)

    def show_substring_dialog(self):
        """Диалог для функции SUBSTRING"""
        self.show_string_function_dialog("SUBSTRING", ["Start position:", "Length (optional):"])

    def show_lpad_dialog(self):
        """Диалог для функции LPAD"""
        self.show_string_function_dialog("LPAD", ["Total length:", "Pad character:"])

    def show_rpad_dialog(self):
        """Диалог для функции RPAD"""
        self.show_string_function_dialog("RPAD", ["Total length:", "Pad character:"])

    def show_string_function_dialog(self, func_name, field_labels):
        """Общий диалог для строковых функций с параметрами"""
        dialog = ctk.CTkToplevel(self.app.window)
        dialog.title(f"{func_name} Function")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.app.window)
        dialog.grab_set()

        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        entries = []
        for label in field_labels:
            ctk.CTkLabel(content, text=label).pack(anchor="w", pady=(5, 0))
            entry = ctk.CTkEntry(content)
            entry.pack(fill="x", pady=(2, 10))
            entries.append(entry)

        def apply_function():
            params = [entry.get() for entry in entries]
            input_text = self.input_string.get().strip()
            
            if not input_text:
                self.show_error("Please enter input text!")
                return

            result = self.calculate_string_function(func_name, input_text, params)
            self.display_function_result(func_name, input_text, result, params)
            dialog.destroy()

        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)

        ctk.CTkButton(buttons_frame, text="Apply", 
                     command=apply_function).pack(side="right", padx=(10, 0))

        ctk.CTkButton(buttons_frame, text="Cancel", 
                     command=dialog.destroy).pack(side="right")

    def calculate_string_function(self, func_name, input_text, params):
        """Вычисление результата строковой функции"""
        try:
            if func_name == "SUBSTRING":
                start = int(params[0]) - 1  # Convert to 0-based index
                length = int(params[1]) if params[1] else None
                if length:
                    return input_text[start:start + length]
                else:
                    return input_text[start:]
                    
            elif func_name == "LPAD":
                length = int(params[0])
                pad_char = params[1] if params[1] else " "
                return input_text.rjust(length, pad_char)
                
            elif func_name == "RPAD":
                length = int(params[0])
                pad_char = params[1] if params[1] else " "
                return input_text.ljust(length, pad_char)
                
        except (ValueError, IndexError) as e:
            return f"Error: {str(e)}"

    def apply_concat(self):
        """Применение функции CONCAT"""
        input_text = self.input_string.get().strip()
        concat_text = self.concat_string.get().strip()
        
        if not input_text or not concat_text:
            self.show_error("Please enter both strings!")
            return

        result = input_text + concat_text
        self.display_function_result("CONCAT", input_text, result, [concat_text])

    def apply_concat_operator(self):
        """Применение оператора ||"""
        input_text = self.input_string.get().strip()
        concat_text = self.concat_string.get().strip()
        
        if not input_text or not concat_text:
            self.show_error("Please enter both strings!")
            return

        result = input_text + concat_text
        self.display_function_result("||", input_text, result, [concat_text])

    def display_function_result(self, func_name, input_text, result, params=None):
        """Отображение результата функции"""
        self.function_results.configure(state="normal")
        
        # Форматируем вывод
        if params:
            params_str = ", ".join([f"'{p}'" for p in params])
            self.function_results.insert("end", f"{func_name}( '{input_text}', {params_str} )\n")
        else:
            self.function_results.insert("end", f"{func_name}( '{input_text}' )\n")
            
        self.function_results.insert("end", f"Result: '{result}'\n")
        self.function_results.insert("end", "-" * 30 + "\n")
        
        self.function_results.see("end")
        self.function_results.configure(state="disabled")

    def show_error(self, message):
        """Показ ошибки"""
        self.status_label.configure(text="❌ Error")
        self.app.show_error(message)

# Не забудьте добавить импорт tkinter
import tkinter as tk