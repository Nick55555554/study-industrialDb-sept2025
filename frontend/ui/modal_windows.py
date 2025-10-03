import customtkinter as ctk
from tkinter import ttk
from typing import List, Dict, Any, Optional
import threading
from tkinter import messagebox
import re


class ModalWindow:
    """Базовый класс для модальных окон"""

    def __init__(self, parent, title: str, width: int = 600, height: int = 500):
        self.parent = parent
        self.title = title

        # Получаем корневое окно из родительского виджета
        self.root = self.get_root_window(parent)

        # Создаем модальное окно
        self.modal = ctk.CTkToplevel(self.root)
        self.modal.title(title)
        self.modal.geometry(f"{width}x{height}")
        self.modal.resizable(False, False)
        self.modal.minsize(width, height)

        # Делаем окно модальным
        self.modal.transient(self.root)
        self.modal.grab_set()

        # Центрируем окно
        self.center_window(width, height)

        # Блокируем родительское окно
        self.root.attributes('-disabled', True)

        # Обработчик закрытия окна
        self.modal.protocol("WM_DELETE_WINDOW", self.on_close)

        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self.modal)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def get_root_window(self, widget):
        """Получаем корневое окно из виджета"""
        current = widget
        while hasattr(current, 'master') and current.master:
            current = current.master
        return current

    def center_window(self, width, height):
        """Центрирование окна относительно родителя"""
        self.modal.update_idletasks()
        x = (self.modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self.modal.winfo_screenheight() // 2) - (height // 2)
        self.modal.geometry(f'{width}x{height}+{x}+{y}')

    def on_close(self):
        """Обработчик закрытия окна"""
        self.root.attributes('-disabled', False)
        self.modal.destroy()


class AddAttackModal(ModalWindow):
    """Модальное окно для добавления новой атаки"""

    def __init__(self, parent, app):
        super().__init__(parent, "Добавить новую атаку", 700, 650)
        self.app = app
        self.target_fields = []
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Добавить новую DDoS атаку",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Создаем скроллируемую область для формы
        self.create_scrollable_form()

    def create_scrollable_form(self):
        """Создание скроллируемой формы"""
        # Основной контейнер для скролла
        container = ctk.CTkFrame(self.main_frame)
        container.pack(fill="both", expand=True, pady=(0, 15))

        # Скроллируемый фрейм
        self.scrollable_frame = ctk.CTkScrollableFrame(container, height=450)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Создаем секции формы
        self.create_basic_info_section()
        self.create_network_info_section()
        self.create_targets_section()
        self.create_mitigation_section()

        # Кнопки действий
        self.create_action_buttons()

    def create_basic_info_section(self):
        """Создание секции основной информации"""
        basic_frame = ctk.CTkFrame(self.scrollable_frame)
        basic_frame.pack(fill="x", pady=10, padx=5)

        # Заголовок секции
        section_label = ctk.CTkLabel(
            basic_frame,
            text="📋 Основная информация",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        section_label.pack(anchor="w", pady=(10, 15))

        # Название атаки
        name_frame = ctk.CTkFrame(basic_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(name_frame, text="Название атаки *").pack(anchor="w")
        self.name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="Например: SYN Flood Attack",
            height=35
        )
        self.name_entry.pack(fill="x", pady=(5, 10))

        # Параметры атаки в сетке
        params_frame = ctk.CTkFrame(basic_frame, fg_color="transparent")
        params_frame.pack(fill="x", pady=5, padx=10)

        # Тип атаки
        ctk.CTkLabel(params_frame, text="Тип атаки *").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        self.type_combo = ctk.CTkComboBox(
            params_frame,
            values=self.app.attack_types,
            width=200,
            height=35
        )
        self.type_combo.grid(row=0, column=1, sticky="w", pady=5)
        self.type_combo.set("volumetric")

        # Уровень опасности
        ctk.CTkLabel(params_frame, text="Уровень опасности *").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.danger_combo = ctk.CTkComboBox(
            params_frame,
            values=self.app.danger_levels,
            width=200,
            height=35
        )
        self.danger_combo.grid(row=1, column=1, sticky="w", pady=5)
        self.danger_combo.set("medium")

        # Частота
        ctk.CTkLabel(params_frame, text="Частота атаки *").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        self.frequency_combo = ctk.CTkComboBox(
            params_frame,
            values=self.app.frequency_levels,
            width=200,
            height=35
        )
        self.frequency_combo.grid(row=2, column=1, sticky="w", pady=5)
        self.frequency_combo.set("medium")

    def create_network_info_section(self):
        """Создание секции сетевой информации"""
        network_frame = ctk.CTkFrame(self.scrollable_frame)
        network_frame.pack(fill="x", pady=10, padx=5)

        # Заголовок секции
        section_label = ctk.CTkLabel(
            network_frame,
            text="🌐 Сетевая информация",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        section_label.pack(anchor="w", pady=(10, 15))

        # IP адреса источников
        ips_frame = ctk.CTkFrame(network_frame, fg_color="transparent")
        ips_frame.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(ips_frame, text="IP адреса источников *").pack(anchor="w")
        ctk.CTkLabel(
            ips_frame,
            text="По одному IP на строку. Пример:\n192.168.1.1\n10.0.0.5",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        self.source_ips_text = ctk.CTkTextbox(ips_frame, height=80)
        self.source_ips_text.pack(fill="x", pady=(5, 10))

        # Порты
        ports_frame = ctk.CTkFrame(network_frame, fg_color="transparent")
        ports_frame.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(ports_frame, text="Затронутые порты").pack(anchor="w")
        ctk.CTkLabel(
            ports_frame,
            text="Через запятую. Пример: 80, 443, 22, 8080",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        self.ports_entry = ctk.CTkEntry(
            ports_frame,
            placeholder_text="80, 443, 22",
            height=35
        )
        self.ports_entry.pack(fill="x", pady=(5, 5))

    def create_targets_section(self):
        """Создание секции целей"""
        targets_frame = ctk.CTkFrame(self.scrollable_frame)
        targets_frame.pack(fill="x", pady=10, padx=5)

        # Заголовок секции
        section_label = ctk.CTkLabel(
            targets_frame,
            text="🎯 Цели атаки",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        section_label.pack(anchor="w", pady=(10, 15))

        # Контейнер для динамического добавления целей
        self.targets_container = ctk.CTkFrame(targets_frame, fg_color="transparent")
        self.targets_container.pack(fill="x", pady=5, padx=10)

        # Кнопка добавления цели
        add_target_btn = ctk.CTkButton(
            targets_frame,
            text="+ Добавить цель",
            command=self.add_target_field,
            fg_color=self.app.colors["success"],
            height=35
        )
        add_target_btn.pack(pady=10)

        # Добавляем первое поле цели по умолчанию
        self.add_target_field()

    def add_target_field(self):
        """Добавление поля для ввода цели"""
        target_frame = ctk.CTkFrame(self.targets_container, fg_color="transparent")
        target_frame.pack(fill="x", pady=5)

        # Номер цели
        target_number = len(self.target_fields) + 1
        ctk.CTkLabel(target_frame, text=f"Цель #{target_number} *", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        # IP/URL
        ip_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        ip_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(ip_frame, text="IP адрес или домен:", width=120).pack(side="left")
        ip_entry = ctk.CTkEntry(
            ip_frame,
            placeholder_text="192.168.1.1 или example.com",
            height=35
        )
        ip_entry.pack(side="left", fill="x", expand=True, padx=(10, 10))

        # Protocol
        ctk.CTkLabel(ip_frame, text="Протокол:", width=80).pack(side="left")
        protocol_combo = ctk.CTkComboBox(
            ip_frame,
            values=self.app.protocols,
            width=120,
            height=35
        )
        protocol_combo.pack(side="left", padx=(10, 10))
        protocol_combo.set("tcp")

        # Кнопка удаления (только если целей больше одной)
        if len(self.target_fields) > 0:
            remove_btn = ctk.CTkButton(
                ip_frame,
                text="✕",
                width=35,
                height=35,
                fg_color=self.app.colors["danger"],
                command=lambda f=target_frame: self.remove_target_field(f)
            )
            remove_btn.pack(side="left")

        self.target_fields.append({
            'frame': target_frame,
            'ip_entry': ip_entry,
            'protocol_combo': protocol_combo
        })

    def remove_target_field(self, target_frame):
        """Удаление поля цели"""
        for field in self.target_fields:
            if field['frame'] == target_frame:
                field['frame'].destroy()
                self.target_fields.remove(field)
                self.update_target_numbers()
                break

    def update_target_numbers(self):
        """Обновление номеров целей"""
        for i, field in enumerate(self.target_fields):
            # Находим label с номером цели и обновляем его
            for widget in field['frame'].winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Цель #" in widget.cget("text"):
                    widget.configure(text=f"Цель #{i + 1} *")
                    break

    def create_mitigation_section(self):
        """Создание секции стратегий защиты"""
        mitigation_frame = ctk.CTkFrame(self.scrollable_frame)
        mitigation_frame.pack(fill="x", pady=10, padx=5)

        # Заголовок секции
        section_label = ctk.CTkLabel(
            mitigation_frame,
            text="🛡️ Стратегии защиты",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        section_label.pack(anchor="w", pady=(10, 15))

        mitigation_content = ctk.CTkFrame(mitigation_frame, fg_color="transparent")
        mitigation_content.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(mitigation_content, text="Методы защиты (по одному на строку):").pack(anchor="w")
        ctk.CTkLabel(
            mitigation_content,
            text="Пример:\nБлокировка по IP\nОграничение запросов\nФильтрация трафика",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        self.mitigation_text = ctk.CTkTextbox(mitigation_content, height=100)
        self.mitigation_text.pack(fill="x", pady=(5, 5))
        # Добавляем стандартные стратегии по умолчанию
        default_mitigation = "Блокировка подозрительных IP\nОграничение частоты запросов\nФильтрация сетевого трафика\nИспользование WAF"
        self.mitigation_text.insert("1.0", default_mitigation)

    def create_action_buttons(self):
        """Создание кнопок действий"""
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)

        # Левая часть - информация о обязательных полях
        info_label = ctk.CTkLabel(
            buttons_frame,
            text="* - обязательные поля",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(side="left")

        # Правая часть - кнопки действий
        action_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        action_buttons_frame.pack(side="right")

        ctk.CTkButton(
            action_buttons_frame,
            text="Отмена",
            command=self.on_close,
            height=35,
            width=100
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            action_buttons_frame,
            text="Создать атаку",
            command=self.create_attack,
            fg_color=self.app.colors["success"],
            height=35,
            width=120
        ).pack(side="right")

    def get_targets_data(self):
        """Получение данных о целях из формы"""
        targets = []
        for field in self.target_fields:
            ip = field['ip_entry'].get().strip()
            protocol = field['protocol_combo'].get()
            if ip:
                # Определяем, является ли ввод IP-адресом или доменным именем
                if self.is_valid_ip(ip):
                    target_data = {
                        "ip_address": ip,
                        "protocol": protocol,
                        "status": "active"
                    }
                elif self.is_valid_domain(ip):
                    target_data = {
                        "domain": ip,
                        "protocol": protocol,
                        "status": "active"
                    }
                else:
                    # Если не IP и не домен, все равно добавляем как IP
                    target_data = {
                        "ip_address": ip,
                        "protocol": protocol,
                        "status": "active"
                    }
                targets.append(target_data)
        return targets

    def is_valid_ip(self, ip):
        """Проверка валидности IP адреса"""
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        if ip_pattern.match(ip):
            parts = ip.split('.')
            for part in parts:
                if not 0 <= int(part) <= 255:
                    return False
            return True
        return False

    def is_valid_domain(self, domain):
        """Проверка валидности доменного имени"""
        domain_pattern = re.compile(
            r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        )
        return domain_pattern.match(domain) is not None

    def validate_form(self):
        """Валидация формы"""
        errors = []

        # Проверка названия
        name = self.name_entry.get().strip()
        if not name:
            errors.append("Введите название атаки")

        # Проверка IP источников
        source_ips = [ip.strip() for ip in self.source_ips_text.get("1.0", "end-1c").split("\n") if ip.strip()]
        if not source_ips:
            errors.append("Добавьте хотя бы один IP адрес источника")
        else:
            for ip in source_ips:
                if not self.is_valid_ip(ip):
                    errors.append(f"Неверный формат IP адреса: {ip}")

        # Проверка целей
        targets = self.get_targets_data()
        if not targets:
            errors.append("Добавьте хотя бы одну цель")

        # Проверка портов
        ports_text = self.ports_entry.get().strip()
        if ports_text:
            ports = [port.strip() for port in ports_text.split(",") if port.strip()]
            for port in ports:
                if not port.isdigit() or not (1 <= int(port) <= 65535):
                    errors.append(f"Неверный номер порта: {port}")

        return errors

    def create_attack(self):
        """Создание новой атаки"""
        # Валидация формы
        errors = self.validate_form()
        if errors:
            error_message = "\n".join(f"• {error}" for error in errors)
            messagebox.showerror("Ошибки в форме", f"Исправьте следующие ошибки:\n\n{error_message}")
            return

        # Сбор данных
        name = self.name_entry.get().strip()
        source_ips = [ip.strip() for ip in self.source_ips_text.get("1.0", "end-1c").split("\n") if ip.strip()]
        targets = self.get_targets_data()

        ports_text = self.ports_entry.get().strip()
        ports = []
        if ports_text:
            ports = [int(port.strip()) for port in ports_text.split(",") if port.strip().isdigit()]

        mitigation_strategies = [strat.strip() for strat in self.mitigation_text.get("1.0", "end-1c").split("\n") if
                                 strat.strip()]

        # Подготовка данных для API
        attack_data = {
            "name": name,
            "frequency": self.frequency_combo.get(),
            "danger": self.danger_combo.get(),
            "attack_type": self.type_combo.get(),
            "source_ips": source_ips,
            "affected_ports": ports,
            "mitigation_strategies": mitigation_strategies,
            "targets": targets
        }

        self.app.logger.log_info(f"Создание новой атаки: {name}")

        # Создание в отдельном потоке
        def create_thread():
            try:
                result = self.app.api_client.create_attack(attack_data)
                self.app.logger.log_database_operation("CREATE_ATTACK", True)

                # Обновляем UI в основном потоке
                self.modal.after(0, lambda: self.on_creation_success(name))

            except Exception as e:
                self.app.logger.log_error(f"Ошибка создания атаки: {e}")
                self.app.logger.log_database_operation("CREATE_ATTACK", False)
                self.modal.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка создания атаки: {e}"))

        thread = threading.Thread(target=create_thread)
        thread.daemon = True
        thread.start()

    def on_creation_success(self, attack_name):
        """Обработка успешного создания атаки"""
        self.app.refresh_attacks()
        self.app.show_success(f"Атака '{attack_name}' успешно создана!")
        self.on_close()


class DataViewModal(ModalWindow):
    """Модальное окно для просмотра данных с фильтрами"""

    def __init__(self, parent, app):
        super().__init__(parent, "Просмотр данных", 900, 600)
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Просмотр данных атак",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 15))

        # Секция фильтров
        self.create_filters_section()

        # Таблица данных
        self.create_table_section()

    def create_filters_section(self):
        """Создание секции фильтров"""
        filters_frame = ctk.CTkFrame(self.main_frame)
        filters_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(filters_frame, text="Фильтры", font=("Arial", 12, "bold")).pack(anchor="w", pady=8, padx=10)

        # Строка с фильтрами
        filters_row = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filters_row.pack(fill="x", padx=10, pady=(0, 8))

        # Фильтр по типу атаки
        ctk.CTkLabel(filters_row, text="Тип атаки:").pack(side="left", padx=(0, 5))
        self.type_filter = ctk.CTkComboBox(filters_row, values=["Все"] + self.app.attack_types, width=140)
        self.type_filter.pack(side="left", padx=(0, 15))
        self.type_filter.set("Все")

        # Фильтр по уровню опасности
        ctk.CTkLabel(filters_row, text="Опасность:").pack(side="left", padx=(0, 5))
        self.danger_filter = ctk.CTkComboBox(filters_row, values=["Все"] + self.app.danger_levels, width=140)
        self.danger_filter.pack(side="left", padx=(0, 15))
        self.danger_filter.set("Все")

        # Кнопка применения фильтров
        ctk.CTkButton(
            filters_row,
            text="Применить фильтры",
            command=self.apply_filters,
            width=120
        ).pack(side="left")

    def create_table_section(self):
        """Создание секции таблицы"""
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True)

        # Создаем Treeview
        columns = ("name", "type", "danger", "frequency", "sources", "targets", "date")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        # Настраиваем колонки
        columns_config = [
            ("name", "Название", 150),
            ("type", "Тип", 120),
            ("danger", "Опасность", 100),
            ("frequency", "Частота", 100),
            ("sources", "Источники", 120),
            ("targets", "Цели", 80),
            ("date", "Дата", 100)
        ]

        for col_id, heading, width in columns_config:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Упаковка
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Заполняем данными
        self.load_data()

    def load_data(self, filtered_attacks=None):
        """Загрузка данных в таблицу"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Используем переданные данные или все атаки
        attacks = filtered_attacks if filtered_attacks is not None else self.app.attacks

        # Заполняем данными
        for attack in attacks:
            if isinstance(attack, dict):
                sources = attack.get("source_ips", [])
                sources_preview = f"{len(sources)} IP" if len(sources) <= 3 else f"{len(sources)} IP"

                self.tree.insert("", "end", values=(
                    attack.get("name", ""),
                    attack.get("attack_type", ""),
                    attack.get("danger", ""),
                    attack.get("frequency", ""),
                    sources_preview,
                    len(attack.get("targets", [])),
                    attack.get("created_at", "")[:10] if attack.get("created_at") else ""
                ))

    def apply_filters(self):
        """Применение фильтров"""
        try:
            type_filter = self.type_filter.get()
            danger_filter = self.danger_filter.get()

            filtered_attacks = self.app.attacks.copy()

            # Фильтрация по типу атаки
            if type_filter != "Все":
                filtered_attacks = [a for a in filtered_attacks
                                    if a.get("attack_type") == type_filter]

            # Фильтрация по уровню опасности
            if danger_filter != "Все":
                filtered_attacks = [a for a in filtered_attacks
                                    if a.get("danger") == danger_filter]

            self.load_data(filtered_attacks)
            self.app.logger.log_info(f"Применены фильтры: тип={type_filter}, опасность={danger_filter}")

        except Exception as e:
            self.app.logger.log_error(f"Ошибка применения фильтров: {e}")
            messagebox.showerror("Ошибка", f"Ошибка применения фильтров: {e}")