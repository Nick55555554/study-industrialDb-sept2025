import threading


# ... остальной код формы ...

class AttackForm:
    def __init__(self, parent, app):
        self.app = app
        self.target_fields = []
        self.setup_ui(parent)

    # ... остальные методы формы ...

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
                ports = [int(port.strip()) for port in self.ports_entry.get().split(",") if port.strip().isdigit()]
                mitigation_strategies = [strat.strip() for strat in
                                         self.mitigation_text.get("1.0", "end-1c").split("\n") if strat.strip()]
                targets = self.get_targets_data()

                if not source_ips:
                    self.show_error("Please add at least one source IP!")
                    return

                if not targets:
                    self.show_error("Please add at least one target!")
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
                    "targets": [target.__dict__ for target in targets]
                }

                # Отправка на сервер
                result = self.app.api_client.create_attack(attack_data)

                # Обновление UI в основном потоке
                self.app.window.after(0, lambda: self.on_attack_created(result, name))

            except ValueError as e:
                self.app.window.after(0, lambda: self.show_error(f"Invalid input: {e}"))
            except Exception as e:
                self.app.window.after(0, lambda: self.show_error(f"Failed to create attack: {e}"))

        # Запуск в отдельном потоке
        thread = threading.Thread(target=create_attack_thread)
        thread.daemon = True
        thread.start()

    def on_attack_created(self, result, name):
        """Обработка успешного создания атаки"""
        self.app.refresh_attacks()
        self.clear_form()
        self.show_success(f"Attack '{name}' created successfully!")

    def update_attack(self):
        """Обновление существующей атаки через API"""
        if self.app.current_edit_id is None:
            return

        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Please enter attack name!")
            return

        def update_attack_thread():
            try:
                # Сбор данных из формы
                source_ips = [ip.strip() for ip in self.source_ips_text.get("1.0", "end-1c").split("\n") if ip.strip()]
                ports = [int(port.strip()) for port in self.ports_entry.get().split(",") if port.strip().isdigit()]
                mitigation_strategies = [strat.strip() for strat in
                                         self.mitigation_text.get("1.0", "end-1c").split("\n") if strat.strip()]
                targets = self.get_targets_data()

                if not source_ips:
                    self.show_error("Please add at least one source IP!")
                    return

                if not targets:
                    self.show_error("Please add at least one target!")
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
                self.app.window.after(0, lambda: self.show_error(f"Invalid input: {e}"))
            except Exception as e:
                self.app.window.after(0, lambda: self.show_error(f"Failed to update attack: {e}"))

        # Запуск в отдельном потоке
        thread = threading.Thread(target=update_attack_thread)
        thread.daemon = True
        thread.start()

    def on_attack_updated(self, result, name):
        """Обработка успешного обновления атаки"""
        self.app.refresh_attacks()
        self.cancel_edit()
        self.show_success(f"Attack '{name}' updated successfully!")

    def fill_form_data(self, attack):
        """Заполнение формы данными атаки для редактирования"""
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, attack["name"])

        self.frequency_combo.set(attack["frequency"])
        self.danger_combo.set(attack["danger"])
        self.attack_type_combo.set(attack["attack_type"])

        self.source_ips_text.delete("1.0", "end")
        self.source_ips_text.insert("1.0", "\n".join(attack["source_ips"]))

        self.ports_entry.delete(0, "end")
        self.ports_entry.insert(0, ", ".join(map(str, attack["affected_ports"])))

        self.mitigation_text.delete("1.0", "end")
        self.mitigation_text.insert("1.0", "\n".join(attack["mitigation_strategies"]))

        self.set_targets_data(attack["targets"])

        # Активация кнопок редактирования
        self.add_button.configure(state="disabled")
        self.update_button.configure(state="normal")
        self.cancel_button.configure(state="normal")