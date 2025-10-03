import threading


# ... остальной код таблицы ...

class AttackTable:
    def __init__(self, parent, app):
        self.app = app
        self.tree = None
        self.setup_ui(parent)
        self.refresh_table()

    # ... остальные методы таблицы ...

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

        for item in self.tree.get_children():
            self.tree.delete(item)

        for attack in self.app.attacks:
            # Сокращенные данные для таблицы
            source_ips_preview = ", ".join(attack["source_ips"][:2]) + ("..." if len(attack["source_ips"]) > 2 else "")
            ports_preview = ", ".join(map(str, attack["affected_ports"][:3])) + (
                "..." if len(attack["affected_ports"]) > 3 else "")
            targets_count = len(attack["targets"])
            created_date = attack["created_at"][:10] if attack["created_at"] else "Unknown"

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
            ), tags=(attack["id"],))