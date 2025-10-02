import customtkinter as ctk
from models.attack import Attack, Target

class AttackForm:
    def __init__(self, parent, app):
        self.app = app
        self.target_fields = []
        self.setup_ui(parent)
    
    def setup_ui(self, parent):
        """Создание улучшенной формы ввода"""
        # Основной контейнер формы с прокруткой
        form_container = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Создание секций формы
        self.create_basic_info_section(form_container)
        self.create_source_section(form_container)
        self.create_targets_section(form_container)
        self.create_mitigation_section(form_container)
        self.create_action_buttons(form_container)
    
    def create_basic_info_section(self, parent):
        """Секция основной информации"""
        card = self.create_card(parent, "🎯 Basic Attack Information")
        
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=15, pady=15)
        
        # Строка 1
        ctk.CTkLabel(grid, text="Attack Name:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.name_entry = ctk.CTkEntry(grid, width=300, placeholder_text="Enter attack name...")
        self.name_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        
        ctk.CTkLabel(grid, text="Frequency:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=20, pady=8, sticky="w")
        self.frequency_combo = ctk.CTkComboBox(grid, values=self.app.frequency_levels, width=140)
        self.frequency_combo.grid(row=0, column=3, padx=5, pady=8, sticky="w")
        self.frequency_combo.set("high")
        
        # Строка 2
        ctk.CTkLabel(grid, text="Danger Level:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.danger_combo = ctk.CTkComboBox(grid, values=self.app.danger_levels, width=140)
        self.danger_combo.grid(row=1, column=1, padx=5, pady=8, sticky="w")
        self.danger_combo.set("high")
        
        ctk.CTkLabel(grid, text="Attack Type:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=2, padx=20, pady=8, sticky="w")
        self.attack_type_combo = ctk.CTkComboBox(grid, values=self.app.attack_types, width=140)
        self.attack_type_combo.grid(row=1, column=3, padx=5, pady=8, sticky="w")
        self.attack_type_combo.set("amplification")
    
    def create_source_section(self, parent):
        """Секция источников и портов"""
        card = self.create_card(parent, "🌐 Source Configuration")
        
        columns = ctk.CTkFrame(card, fg_color="transparent")
        columns.pack(fill="x", padx=15, pady=15)
        
        # Левая колонка - Source IPs
        left_col = ctk.CTkFrame(columns, fg_color="transparent")
        left_col.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left_col, text="Source IP Addresses:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(left_col, text="One IP address per line", font=ctk.CTkFont(size=12), 
                    text_color=self.app.colors["text_muted"]).pack(anchor="w", pady=(0, 8))
        
        self.source_ips_text = ctk.CTkTextbox(left_col, height=100, border_width=1, fg_color="#2a2a3a")
        self.source_ips_text.pack(fill="x", pady=5)
        self.source_ips_text.insert("1.0", "8.8.8.8\n1.1.1.1\n9.9.9.9")
        
        # Правая колонка - Ports
        right_col = ctk.CTkFrame(columns, fg_color="transparent")
        right_col.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(right_col, text="Affected Ports:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(right_col, text="Comma-separated port numbers", font=ctk.CTkFont(size=12),
                    text_color=self.app.colors["text_muted"]).pack(anchor="w", pady=(0, 8))
        
        self.ports_entry = ctk.CTkEntry(right_col, placeholder_text="53, 80, 443, 8080")
        self.ports_entry.pack(fill="x", pady=5)
        self.ports_entry.insert(0, "53, 443, 80")
    
    def create_targets_section(self, parent):
        """Секция целей"""
        card = self.create_card(parent, "🎯 Attack Targets")
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(header, text="Target Servers & Services", font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        ctk.CTkButton(header, text="+ Add Target", width=100, height=32,
                     command=self.add_target_field).pack(side="right")
        
        self.targets_container = ctk.CTkFrame(card, fg_color="transparent")
        self.targets_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self.add_target_field()
    
    def create_mitigation_section(self, parent):
        """Секция стратегий mitigation"""
        card = self.create_card(parent, "🛡️ Mitigation Strategies")
        
        ctk.CTkLabel(card, text="Defense Mechanisms", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(card, text="One strategy per line", font=ctk.CTkFont(size=12),
                    text_color=self.app.colors["text_muted"]).pack(anchor="w", padx=15, pady=(0, 8))
        
        self.mitigation_text = ctk.CTkTextbox(card, height=120, border_width=1, fg_color="#2a2a3a")
        self.mitigation_text.pack(fill="x", padx=15, pady=(0, 15))
        self.mitigation_text.insert("1.0", "DNS Response Rate Limiting\nAnycast DNS Implementation\nSource IP Validation\nTraffic Filtering")
    
    def create_action_buttons(self, parent):
        """Кнопки действий"""
        card = self.create_card(parent, "")
        
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=15)
        
        self.add_button = ctk.CTkButton(button_frame, text="🚀 Create Attack", 
                                       command=self.create_attack, height=40,
                                       fg_color=self.app.colors["success"], hover_color="#45b7af",
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.add_button.pack(side="left", padx=5)
        
        self.update_button = ctk.CTkButton(button_frame, text="🔄 Update Attack", 
                                         command=self.update_attack, height=40, state="disabled",
                                         fg_color=self.app.colors["warning"], hover_color="#e6b957",
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.update_button.pack(side="left", padx=5)
        
        self.cancel_button = ctk.CTkButton(button_frame, text="❌ Cancel Edit", 
                                         command=self.cancel_edit, height=40, state="disabled",
                                         fg_color=self.app.colors["danger"], hover_color="#e55a5a",
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.cancel_button.pack(side="left", padx=5)
    
    def create_card(self, parent, title):
        """Создание карточки с заголовком"""
        card = ctk.CTkFrame(parent, fg_color=self.app.colors["card_bg"], corner_radius=12)
        card.pack(fill="x", padx=5, pady=8)
        
        if title:
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=15, pady=15)
            ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
            
            # Разделитель
            separator = ctk.CTkFrame(card, height=1, fg_color="#3a3a5a")
            separator.pack(fill="x", padx=15)
        
        return card
    
    def add_target_field(self):
        """Добавление поля для ввода target"""
        target_card = ctk.CTkFrame(self.targets_container, fg_color="#2a2a4a", corner_radius=8)
        target_card.pack(fill="x", pady=8)
        
        target_index = len(self.target_fields)
        
        # Заголовок target с кнопкой удаления
        target_header = ctk.CTkFrame(target_card, fg_color="transparent")
        target_header.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(target_header, text=f"🎯 Target #{target_index + 1}", 
                    font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        if target_index > 0:  # Не показывать кнопку удаления для первого target
            ctk.CTkButton(target_header, text="🗑️ Remove", width=80, height=24,
                         command=lambda: self.remove_target_field(target_card),
                         fg_color=self.app.colors["danger"], hover_color="#e55a5a").pack(side="right")
        
        # Поля для target
        fields_frame = ctk.CTkFrame(target_card, fg_color="transparent")
        fields_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Target IP
        ctk.CTkLabel(fields_frame, text="Target IP:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        target_ip_entry = ctk.CTkEntry(fields_frame, placeholder_text="192.168.1.1", width=180)
        target_ip_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Target Domain
        ctk.CTkLabel(fields_frame, text="Domain:").grid(row=0, column=2, padx=15, pady=5, sticky="w")
        target_domain_entry = ctk.CTkEntry(fields_frame, placeholder_text="example.com", width=180)
        target_domain_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Port
        ctk.CTkLabel(fields_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        port_entry = ctk.CTkEntry(fields_frame, placeholder_text="80", width=80)
        port_entry.grid(row=1, column=1, padx=5, pady=5)
        port_entry.insert(0, "80")
        
        # Protocol
        ctk.CTkLabel(fields_frame, text="Protocol:").grid(row=1, column=2, padx=15, pady=5, sticky="w")
        protocol_combo = ctk.CTkComboBox(fields_frame, values=self.app.protocols, width=120)
        protocol_combo.grid(row=1, column=3, padx=5, pady=5)
        protocol_combo.set("tcp")
        
        # Tags
        ctk.CTkLabel(fields_frame, text="Tags:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tags_entry = ctk.CTkEntry(fields_frame, placeholder_text="web-server,critical,production", width=300)
        tags_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        target_data = {
            'frame': target_card,
            'target_ip': target_ip_entry,
            'target_domain': target_domain_entry,
            'port': port_entry,
            'protocol': protocol_combo,
            'tags': tags_entry
        }
        
        self.target_fields.append(target_data)
    
    def remove_target_field(self, target_frame):
        """Удаление поля target"""
        if len(self.target_fields) > 1:
            for i, target_data in enumerate(self.target_fields):
                if target_data['frame'] == target_frame:
                    self.target_fields.pop(i)
                    target_frame.destroy()
                    break
            
            # Renumber remaining targets
            for i, target_data in enumerate(self.target_fields):
                header_frame = target_data['frame'].winfo_children()[0]
                header_label = header_frame.winfo_children()[0]
                header_label.configure(text=f"🎯 Target #{i + 1}")
    
    def get_targets_data(self):
        """Получение данных о targets из формы"""
        targets = []
        for target_data in self.target_fields:
            target_ip = target_data['target_ip'].get().strip()
            target_domain = target_data['target_domain'].get().strip()
            port = target_data['port'].get().strip()
            protocol = target_data['protocol'].get()
            tags_str = target_data['tags'].get().strip()
            
            if target_ip or target_domain:
                target = Target(
                    target_ip=target_ip,
                    target_domain=target_domain,
                    port=int(port) if port.isdigit() else 80,
                    protocol=protocol,
                    tags=[tag.strip() for tag in tags_str.split(",") if tag.strip()]
                )
                targets.append(target)
        
        return targets
    
    def set_targets_data(self, targets):
        """Установка данных о targets в форму"""
        # Очищаем существующие поля
        for target_data in self.target_fields:
            target_data['frame'].destroy()
        self.target_fields = []
        
        # Добавляем поля для каждого target
        for target in targets:
            self.add_target_field()
            last_index = len(self.target_fields) - 1
            
            self.target_fields[last_index]['target_ip'].delete(0, 'end')
            self.target_fields[last_index]['target_ip'].insert(0, target.get('target_ip', ''))
            
            self.target_fields[last_index]['target_domain'].delete(0, 'end')
            self.target_fields[last_index]['target_domain'].insert(0, target.get('target_domain', ''))
            
            self.target_fields[last_index]['port'].delete(0, 'end')
            self.target_fields[last_index]['port'].insert(0, str(target.get('port', 80)))
            
            self.target_fields[last_index]['protocol'].set(target.get('protocol', 'tcp'))
            
            self.target_fields[last_index]['tags'].delete(0, 'end')
            self.target_fields[last_index]['tags'].insert(0, ','.join(target.get('tags', [])))
    
    def create_attack(self):
        """Создание новой атаки"""
        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Please enter attack name!")
            return
        
        try:
            # Сбор данных из формы
            source_ips = [ip.strip() for ip in self.source_ips_text.get("1.0", "end-1c").split("\n") if ip.strip()]
            ports = [int(port.strip()) for port in self.ports_entry.get().split(",") if port.strip().isdigit()]
            mitigation_strategies = [strat.strip() for strat in self.mitigation_text.get("1.0", "end-1c").split("\n") if strat.strip()]
            targets = self.get_targets_data()
            
            if not source_ips:
                self.show_error("Please add at least one source IP!")
                return
            
            if not targets:
                self.show_error("Please add at least one target!")
                return
            
            # Создание объекта атаки
            new_attack = Attack(
                name=name,
                frequency=self.frequency_combo.get(),
                danger=self.danger_combo.get(),
                attack_type=self.attack_type_combo.get(),
                source_ips=source_ips,
                affected_ports=ports,
                mitigation_strategies=mitigation_strategies,
                targets=targets
            )
            
            self.app.attacks.append(new_attack.to_dict())
            self.app.save_data()
            self.app.update_stats()
            self.clear_form()
            self.show_success(f"Attack '{name}' created successfully!")
            
        except ValueError as e:
            self.show_error(f"Invalid input: {e}")
    
    def update_attack(self):
        """Обновление существующей атаки"""
        if self.app.current_edit_id is None:
            return
        
        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Please enter attack name!")
            return
        
        try:
            # Сбор данных из формы
            source_ips = [ip.strip() for ip in self.source_ips_text.get("1.0", "end-1c").split("\n") if ip.strip()]
            ports = [int(port.strip()) for port in self.ports_entry.get().split(",") if port.strip().isdigit()]
            mitigation_strategies = [strat.strip() for strat in self.mitigation_text.get("1.0", "end-1c").split("\n") if strat.strip()]
            targets = self.get_targets_data()
            
            if not source_ips:
                self.show_error("Please add at least one source IP!")
                return
            
            if not targets:
                self.show_error("Please add at least one target!")
                return
            
            # Обновление атаки
            for attack in self.app.attacks:
                if attack["id"] == self.app.current_edit_id:
                    attack.update({
                        "name": name,
                        "frequency": self.frequency_combo.get(),
                        "danger": self.danger_combo.get(),
                        "attack_type": self.attack_type_combo.get(),
                        "source_ips": source_ips,
                        "affected_ports": ports,
                        "mitigation_strategies": mitigation_strategies,
                        "targets": [target.__dict__ for target in targets],
                        "updated_at": self.app.get_current_timestamp()
                    })
                    break
            
            self.app.save_data()
            self.cancel_edit()
            self.app.update_stats()
            self.show_success(f"Attack '{name}' updated successfully!")
            
        except ValueError as e:
            self.show_error(f"Invalid input: {e}")
    
    def cancel_edit(self):
        """Отмена редактирования"""
        self.app.current_edit_id = None
        self.clear_form()
        self.add_button.configure(state="normal")
        self.update_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")
    
    def clear_form(self):
        """Очистка формы"""
        self.name_entry.delete(0, "end")
        self.frequency_combo.set("high")
        self.danger_combo.set("high")
        self.attack_type_combo.set("amplification")
        self.source_ips_text.delete("1.0", "end")
        self.source_ips_text.insert("1.0", "8.8.8.8\n1.1.1.1\n9.9.9.9")
        self.ports_entry.delete(0, "end")
        self.ports_entry.insert(0, "53, 443, 80")
        self.mitigation_text.delete("1.0", "end")
        self.mitigation_text.insert("1.0", "DNS Response Rate Limiting\nAnycast DNS Implementation\nSource IP Validation\nTraffic Filtering")
        
        # Очистка targets (оставляем один пустой)
        for target_data in self.target_fields:
            target_data['frame'].destroy()
        self.target_fields = []
        self.add_target_field()
    
    def show_error(self, message):
        """Показ ошибки"""
        # Реализация показа ошибки
        print(f"❌ {message}")
    
    def show_success(self, message):
        """Показ успеха"""
        print(f"✅ {message}")