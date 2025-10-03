import customtkinter as ctk
from ui.modal_windows import AddAttackModal, DataViewModal


class MainWindow:
    def __init__(self, parent, app):
        self.app = app
        self.parent = parent
        self.setup_main_window()

    def setup_main_window(self):
        """Настройка главного окна с кнопками"""
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame,
            text="Управление базой данных DDoS атак",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 30))

        # Кнопки управления БД
        self.create_database_controls(main_frame)

    def create_database_controls(self, parent):
        """Создание кнопок управления БД"""
        controls_frame = ctk.CTkFrame(parent, fg_color="transparent")
        controls_frame.pack(fill="x", pady=20)

        # Кнопка создания схемы и таблиц
        ctk.CTkButton(
            controls_frame,
            text="Создать схему и таблицы",
            command=self.create_schema,
            fg_color=self.app.colors["primary"],
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(fill="x", pady=10)

        # Кнопка добавления данных (новое модальное окно)
        ctk.CTkButton(
            controls_frame,
            text="Добавить новую атаку",
            command=self.open_add_attack_modal,
            fg_color=self.app.colors["success"],
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(fill="x", pady=10)

        # Кнопка показа данных (отдельное окно)
        ctk.CTkButton(
            controls_frame,
            text="Просмотреть данные",
            command=self.open_data_view_modal,
            fg_color=self.app.colors["warning"],
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(fill="x", pady=10)

    def create_schema(self):
        """Создание схемы БД"""
        try:
            self.app.logger.log_info("Создание схемы базы данных...")
            result = self.app.api_client.initialize_database()

            if result.get('success') or result.get('status') == 'already_exists':
                self.app.logger.log_database_operation("CREATE_SCHEMA", True)
                if result.get('status') == 'already_exists':
                    self.app.show_success("Таблицы уже существуют в базе данных!")
                else:
                    self.app.show_success("Схема базы данных успешно создана!")
            else:
                self.app.logger.log_database_operation("CREATE_SCHEMA", False)
                self.app.show_error("Не удалось создать схему базы данных")

        except Exception as e:
            # Если таблицы уже существуют - это не ошибка
            if "409" in str(e) or "already exists" in str(e).lower():
                self.app.logger.log_database_operation("CREATE_SCHEMA", True)
                self.app.show_success("Таблицы уже существуют в базе данных!")
            else:
                self.app.logger.log_error(f"Ошибка создания схемы БД: {e}")
                self.app.logger.log_database_operation("CREATE_SCHEMA", False)
                self.app.show_error(f"Ошибка создания схемы: {e}")

    def open_add_attack_modal(self):
        """Открытие модального окна добавления новой атаки"""
        self.app.logger.log_info("Открытие модального окна добавления атаки")
        AddAttackModal(self.parent, self.app)

    def open_data_view_modal(self):
        """Открытие модального окна просмотра данных"""
        self.app.logger.log_info("Открытие модального окна просмотра данных")
        DataViewModal(self.parent, self.app)