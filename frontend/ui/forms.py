import customtkinter as ctk
from typing import List, Dict, Any
import threading
from models.attack import Attack
from tkinter import messagebox


class AttackForm:
    def __init__(self, parent, app):
        self.app = app
        self.parent = parent
        self.target_fields = []
        self.setup_ui(parent)  # Этот метод должен существовать!

    def setup_ui(self, parent):
        """Настройка пользовательского интерфейса формы"""
        try:
            # Основной фрейм формы
            self.form_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
            self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Заголовок
            title_label = ctk.CTkLabel(
                self.form_frame,
                text="Create New DDoS Attack",
                font=("Arial", 20, "bold")
            )
            title_label.pack(pady=(0, 20))

            # Создание полей формы
            self.create_basic_info_section()
            self.create_network_info_section()
            self.create_targets_section()
            self.create_mitigation_section()
            self.create_buttons_section()

        except Exception as e:
            print(f"Error setting up form UI: {e}")
            raise

    def create_basic_info_section(self):
        """Создание секции основной информации"""
        basic_frame = ctk.CTkFrame(self.form_frame)
        basic_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(basic_frame, text="Basic Information", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        # Поле имени атаки
        ctk.CTkLabel(basic_frame, text="Attack Name *").pack(anchor="w")
        self.name_entry = ctk.CTkEntry(basic_frame, placeholder_text="Enter attack name")
        self.name_entry.pack(fill="x", pady=(5, 10))

        # Комбо-боксы
        options_frame = ctk.CTkFrame(basic_frame, fg_color="transparent")
        options_frame.pack(fill="x", pady=5)

        # Frequency
        ctk.CTkLabel(options_frame, text="Frequency").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.frequency_combo = ctk.CTkComboBox(options_frame, values=self.app.frequency_levels)
        self.frequency_combo.grid(row=0, column=1, sticky="w", padx=(0, 20))
        self.frequency_combo.set("medium")

        # Danger
        ctk.CTkLabel(options_frame, text="Danger Level").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.danger_combo = ctk.CTkComboBox(options_frame, values=self.app.danger_levels)
        self.danger_combo.grid(row=0, column=3, sticky="w")
        self.danger_combo.set("medium")

        # Attack Type
        ctk.CTkLabel(options_frame, text="Attack Type").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.attack_type_combo = ctk.CTkComboBox(options_frame, values=self.app.attack_types)
        self.attack_type_combo.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        self.attack_type_combo.set("volumetric")

    def create_network_info_section(self):
        """Создание секции сетевой информации"""
        network_frame = ctk.CTkFrame(self.form_frame)
        network_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(network_frame, text="Network Information", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        # Source IPs
        ctk.CTkLabel(network_frame, text="Source IPs * (one per line)").pack(anchor="w")
        self.source_ips_text = ctk.CTkTextbox(network_frame, height=80)
        self.source_ips_text.pack(fill="x", pady=(5, 10))

        # Ports
        ctk.CTkLabel(network_frame, text="Affected Ports (comma separated)").pack(anchor="w")
        self.ports_entry = ctk.CTkEntry(network_frame, placeholder_text="80, 443, 22")
        self.ports_entry.pack(fill="x", pady=(5, 10))

    def create_targets_section(self):
        """Создание секции целей"""
        targets_frame = ctk.CTkFrame(self.form_frame)
        targets_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(targets_frame, text="Targets *", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        # Контейнер для полей целей
        self.targets_container = ctk.CTkFrame(targets_frame, fg_color="transparent")
        self.targets_container.pack(fill="x")

        # Кнопка добавления цели
        ctk.CTkButton(
            targets_frame,
            text="+ Add Target",
            command=self.add_target_field
        ).pack(pady=10)

        # Добавляем первое поле цели по умолчанию
        self.add_target_field()

    def create_mitigation_section(self):
        """Создание секции стратегий mitigation"""
        mitigation_frame = ctk.CTkFrame(self.form_frame)
        mitigation_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(mitigation_frame, text="Mitigation Strategies", font=("Arial", 16, "bold")).pack(anchor="w",
                                                                                                      pady=10)

        ctk.CTkLabel(mitigation_frame, text="Strategies (one per line)").pack(anchor="w")
        self.mitigation_text = ctk.CTkTextbox(mitigation_frame, height=80)
        self.mitigation_text.pack(fill="x", pady=(5, 10))

    def create_buttons_section(self):
        """Создание секции кнопок"""
        buttons_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)

        # Кнопки действий
        self.add_button = ctk.CTkButton(
            buttons_frame,
            text="Create Attack",
            command=self.create_attack,
            fg_color=self.app.colors["success"]
        )
        self.add_button.pack(side="right", padx=(10, 0))

        self.update_button = ctk.CTkButton(
            buttons_frame,
            text="Update Attack",
            command=self.update_attack,
            fg_color=self.app.colors["warning"],
            state="disabled"
        )
        self.update_button.pack(side="right", padx=(10, 0))

        self.cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.cancel_edit,
            fg_color=self.app.colors["danger"]
        )
        self.cancel_button.pack(side="right")
        self.cancel_button.configure(state="disabled")

    def add_target_field(self):
        """Добавление поля для ввода цели"""
        target_frame = ctk.CTkFrame(self.targets_container, fg_color="transparent")
        target_frame.pack(fill="x", pady=5)

        # IP/URL
        ctk.CTkLabel(target_frame, text="Target IP/URL *", width=100).pack(side="left", padx=(0, 10))
        ip_entry = ctk.CTkEntry(target_frame, placeholder_text="192.168.1.1 or example.com")
        ip_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Protocol
        ctk.CTkLabel(target_frame, text="Protocol", width=80).pack(side="left", padx=(0, 10))
        protocol_combo = ctk.CTkComboBox(target_frame, values=self.app.protocols, width=100)
        protocol_combo.pack(side="left", padx=(0, 10))
        protocol_combo.set("http")

        # Кнопка удаления
        remove_btn = ctk.CTkButton(
            target_frame,
            text="×",
            width=30,
            height=30,
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
        if len(self.target_fields) > 1:  # Не удаляем последнее поле
            for field in self.target_fields:
                if field['frame'] == target_frame:
                    field['frame'].destroy()
                    self.target_fields.remove(field)
                    break

    def get_targets_data(self):
        """Получение данных о целях из формы"""
        targets = []
        for field in self.target_fields:
            ip = field['ip_entry'].get().strip()
            protocol = field['protocol_combo'].get()
            if ip:
                # Определяем, является ли ввод IP-адресом или доменным именем
                if self.is_ip_address(ip):
                    target_data = {
                        "target_ip": ip,
                        "target_domain": None,
                        "protocol": protocol,
                        "tags": {}
                    }
                else:
                    target_data = {
                        "target_ip": None,
                        "target_domain": ip,
                        "protocol": protocol,
                        "tags": {}
                    }
                targets.append(target_data)
        return targets

    def is_ip_address(self, value):
        """Проверяет, является ли строка IP-адресом"""
        import re
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        return ip_pattern.match(value) is not None

    def set_targets_data(self, targets_data):
        """Заполнение полей целей данными"""
        # Очищаем существующие поля (кроме первого)
        while len(self.target_fields) > 1:
            self.remove_target_field(self.target_fields[-1]['frame'])

        # Заполняем первое поле
        if targets_data:
            first_target = targets_data[0]
            self.target_fields[0]['ip_entry'].delete(0, 'end')
            self.target_fields[0]['ip_entry'].insert(0, first_target.get('ip_address', ''))
            self.target_fields[0]['protocol_combo'].set(first_target.get('protocol', 'http'))

            # Добавляем остальные цели
            for target_data in targets_data[1:]:
                self.add_target_field()
                self.target_fields[-1]['ip_entry'].insert(0, target_data.get('ip_address', ''))
                self.target_fields[-1]['protocol_combo'].set(target_data.get('protocol', 'http'))

    def create_attack(self):
        """Создание новой атаки через API"""
        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Please enter attack name!")
            return

        def create_attack_thread():
            try:
                # Сбор данных из формы
                source_ips = [ip.strip() for ip in self.source_ips_text.get("1.0", "end-1c").split("\n") if ip.strip()]
                ports_text = self.ports_entry.get().strip()
                ports = []
                if ports_text:
                    ports = [int(port.strip()) for port in ports_text.split(",") if port.strip().isdigit()]

                mitigation_strategies = [strat.strip() for strat in
                                         self.mitigation_text.get("1.0", "end-1c").split("\n") if strat.strip()]
                targets = self.get_targets_data()

                # Валидация данных
                if not source_ips:
                    self.app.window.after(0, lambda: self.show_error("Please add at least one source IP!"))
                    return

                if not targets:
                    self.app.window.after(0, lambda: self.show_error("Please add at least one target!"))
                    return

                # Подготовка данных для API
                attack_data = {
                    "name": name,
                    "frequency": self.frequency_combo.get(),
                    "danger": self.danger_combo.get(),
                    "attack_type": self.attack_type_combo.get(),
                    "source_ips": source_ips,
                    "affected_ports": ports,
                    "mitigation_strategies": mitigation_strategies,
                    "targets": [target for target in targets]
                }

                print(f"Sending attack data: {attack_data}")  # Для отладки

                # Отправка на сервер
                result = self.app.api_client.create_attack(attack_data)
                print(f"Server response: {result}")  # Для отладки

                # Обновление UI в основном потоке
                self.app.window.after(0, lambda: self.on_attack_created(result, name))

            except ValueError as e:
                error_msg = f"Invalid input: {e}"
                self.app.window.after(0, lambda msg=error_msg: self.show_error(msg))
            except Exception as e:
                error_msg = f"Failed to create attack: {e}"
                self.app.window.after(0, lambda msg=error_msg: self.show_error(msg))

        # Запуск в отдельном потоке
        thread = threading.Thread(target=create_attack_thread)
        thread.daemon = True
        thread.start()

    def on_attack_created(self, result, name):
        """Обработка успешного создания атаки"""
        self.app.refresh_attacks()
        self.clear_form()
        self.show_success(f"Attack '{name}' created successfully!")
        # Переключаемся на список атак чтобы увидеть результат
        self.app.show_attacks_list()

    def update_attack(self):
        """Обновление существующей атаки через API"""
        if self.app.current_edit_id is None:
            self.show_error("No attack selected for editing!")
            return

        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Please enter attack name!")
            return

        def update_attack_thread():
            try:
                # Сбор данных из формы
                source_ips = [ip.strip() for ip in self.source_ips_text.get("1.0", "end-1c").split("\n") if ip.strip()]
                ports_text = self.ports_entry.get().strip()
                ports = []
                if ports_text:
                    ports = [int(port.strip()) for port in ports_text.split(",") if port.strip().isdigit()]

                mitigation_strategies = [strat.strip() for strat in
                                         self.mitigation_text.get("1.0", "end-1c").split("\n") if strat.strip()]
                targets = self.get_targets_data()

                if not source_ips:
                    self.app.window.after(0, lambda: self.show_error("Please add at least one source IP!"))
                    return

                if not targets:
                    self.app.window.after(0, lambda: self.show_error("Please add at least one target!"))
                    return

                # Подготовка данных для обновления с целями
                update_data = {
                    "attack": {
                        "name": name,
                        "frequency": self.frequency_combo.get(),
                        "danger": self.danger_combo.get(),
                        "attack_type": self.attack_type_combo.get(),
                        "source_ips": source_ips,
                        "affected_ports": ports,
                        "mitigation_strategies": mitigation_strategies
                    },
                    "targets": [target.__dict__ for target in targets]
                }

                # Отправка на сервер
                result = self.app.api_client.update_attack_with_targets(
                    self.app.current_edit_id, update_data
                )

                # Обновление UI в основном потоке
                self.app.window.after(0, lambda: self.on_attack_updated(result, name))

            except ValueError as e:
                error_msg = f"Invalid input: {e}"
                self.app.window.after(0, lambda msg=error_msg: self.show_error(msg))
            except Exception as e:
                error_msg = f"Failed to update attack: {e}"
                self.app.window.after(0, lambda msg=error_msg: self.show_error(msg))

        # Запуск в отдельном потоке
        thread = threading.Thread(target=update_attack_thread)
        thread.daemon = True
        thread.start()

    def on_attack_updated(self, result, name):
        """Обработка успешного обновления атаки"""
        self.app.refresh_attacks()
        self.cancel_edit()
        self.show_success(f"Attack '{name}' updated successfully!")
        # Переключаемся на список атак
        self.app.show_attacks_list()

    def cancel_edit(self):
        """Отмена редактирования"""
        self.app.current_edit_id = None
        self.clear_form()
        # Активируем кнопку создания, деактивируем кнопки редактирования
        self.add_button.configure(state="normal")
        self.update_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")

    def clear_form(self):
        """Очистка формы"""
        self.name_entry.delete(0, "end")
        self.frequency_combo.set("medium")
        self.danger_combo.set("medium")
        self.attack_type_combo.set("flood")
        self.source_ips_text.delete("1.0", "end")
        self.ports_entry.delete(0, "end")
        self.mitigation_text.delete("1.0", "end")

        # Очищаем цели (оставляем только одно пустое поле)
        while len(self.target_fields) > 1:
            self.remove_target_field(self.target_fields[-1]['frame'])
        if self.target_fields:
            self.target_fields[0]['ip_entry'].delete(0, "end")
            self.target_fields[0]['protocol_combo'].set("http")

    def fill_form_data(self, attack):
        """Заполнение формы данными атаки для редактирования"""
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, attack.get("name", ""))

        self.frequency_combo.set(attack.get("frequency", "medium"))
        self.danger_combo.set(attack.get("danger", "medium"))
        self.attack_type_combo.set(attack.get("attack_type", "flood"))

        self.source_ips_text.delete("1.0", "end")
        self.source_ips_text.insert("1.0", "\n".join(attack.get("source_ips", [])))

        self.ports_entry.delete(0, "end")
        ports = attack.get("affected_ports", [])
        self.ports_entry.insert(0, ", ".join(map(str, ports)))

        self.mitigation_text.delete("1.0", "end")
        self.mitigation_text.insert("1.0", "\n".join(attack.get("mitigation_strategies", [])))

        self.set_targets_data(attack.get("targets", []))

        # Активация кнопок редактирования
        self.add_button.configure(state="disabled")
        self.update_button.configure(state="normal")
        self.cancel_button.configure(state="normal")

    def show_error(self, message):
        """Показ ошибки"""
        messagebox.showerror("Error", message)

    def show_success(self, message):
        """Показ успеха"""
        messagebox.showinfo("Success", message)