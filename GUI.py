import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QScrollArea,
                             QLineEdit, QTextEdit, QMessageBox, QDateEdit)
from PyQt6.QtCore import Qt, QTimer, QDate
from database import PlantDatabase
from styles import Styles


def create_styled_button(text, style, icon=""):
    button_text = f"{icon} {text}" if icon else text
    button = QPushButton(button_text)
    button.setStyleSheet(style)
    return button


def create_styled_input(field_type, placeholder="", text=""):
    if field_type == "line":
        field = QLineEdit()
        field.setText(text)
        if placeholder:
            field.setPlaceholderText(placeholder)
    else:
        field = QTextEdit()
        field.setPlainText(text)
        if placeholder:
            field.setPlaceholderText(placeholder)
        field.setMaximumHeight(100)

    field.setStyleSheet(Styles.INPUT_STYLE)
    return field


def create_title(text):
    title = QLabel(text)
    title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3e2723;")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return title


def create_card_frame():
    card = QFrame()
    card.setStyleSheet(Styles.CARD_STYLE)
    return card


def create_form_frame():
    form_frame = QFrame()
    form_frame.setStyleSheet(f"""
        QFrame {{
            background-color: {Styles.WHITE};
            padding: 20px;
            border-radius: 10px;
            border: 2px solid {Styles.LIGHT_GREEN};
        }}
    """)
    return form_frame


def create_form_section(title, widget):
    layout = QVBoxLayout()
    label = QLabel(title)
    label.setStyleSheet("font-weight: bold; color: #3e2723; margin-top: 10px;")
    layout.addWidget(label)
    layout.addWidget(widget)
    return layout


def create_date_edit():
    """Create a styled date selection widget"""
    date_edit = QDateEdit()
    date_edit.setDate(QDate.currentDate())
    date_edit.setCalendarPopup(True)
    date_edit.setStyleSheet(f"""
        QDateEdit {{
            padding: 12px;
            border: 2px solid {Styles.LIGHT_BROWN};
            border-radius: 8px;
            font-size: 14px;
            background-color: {Styles.WHITE};
            color: {Styles.DARK_TEXT};
        }}
        QDateEdit:focus {{
            border-color: {Styles.PRIMARY_GREEN};
            background-color: {Styles.LIGHT_GREEN};
        }}
    """)
    return date_edit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = PlantDatabase()
        self.setup_ui()
        self.setup_watering_timer()

    def setup_watering_timer(self):
        """Setup timer to check for watering status updates"""
        self.watering_timer = QTimer()
        self.watering_timer.timeout.connect(self.check_watering_status)
        self.watering_timer.start(60000)  # Check every minute

    def check_watering_status(self):
        """Check if we need to refresh watering status (new day)"""
        # This will automatically handle day changes
        if hasattr(self, 'current_plants_display'):
            self.show_plant_list()

    def setup_ui(self):
        self.setWindowTitle("🌿 Plant Growth Tracker")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(Styles.MAIN_STYLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.show_plant_list()

    def show_plant_list(self):
        self.clear_layout()

        # Title
        self.main_layout.addWidget(create_title("🌿 My Plants"))

        # Add Plant Button
        add_btn = create_styled_button("Add New Plant", Styles.PRIMARY_BUTTON, "➕")
        add_btn.clicked.connect(self.show_add_plant_form)
        self.main_layout.addWidget(add_btn)

        # Plants container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        plants = self.db.get_all_plants()

        if plants:
            for plant in plants:
                plant_card = self.create_plant_card(plant)
                scroll_layout.addWidget(plant_card)
        else:
            no_plants = QLabel("No plants yet! Click 'Add New Plant' to start. 🌱")
            no_plants.setStyleSheet("color: #8d6e63; font-size: 14px;")
            no_plants.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scroll_layout.addWidget(no_plants)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll_area)

        self.current_plants_display = plants  # Track current display

    def create_plant_card(self, plant):
        plant_id, name, date_planted, care_plan, last_watered, created_at = plant

        card = create_card_frame()
        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # Plant info
        name_label = QLabel(f"<b>Plant Name:</b> {name}")
        name_label.setStyleSheet("font-size: 16px; color: #2e7d32;")
        layout.addWidget(name_label)

        date_label = QLabel(f"<b>Planted:</b> {date_planted}")
        date_label.setStyleSheet("font-size: 14px; color: #795548; font-weight: bold;")
        layout.addWidget(date_label)

        # Watering status
        watering_status = self.get_watering_status(plant)
        status_label = QLabel(watering_status["text"])
        status_label.setStyleSheet(watering_status["style"])
        layout.addWidget(status_label)

        if care_plan:
            care_label = QLabel(f"<b>Care Instructions:</b> {care_plan}")
            care_label.setStyleSheet("font-size: 13px; color: #8d6e63;")
            care_label.setWordWrap(True)
            layout.addWidget(care_label)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        details_btn = create_styled_button("Details", Styles.ACTION_BUTTON, "🔍")
        details_btn.clicked.connect(lambda: self.show_plant_details(plant))
        button_layout.addWidget(details_btn)

        # Water button
        if self.db.needs_watering(plant):
            water_btn = create_styled_button("Water", Styles.PRIMARY_BUTTON, "💧")
            water_btn.clicked.connect(lambda: self.water_plant(plant_id))
            button_layout.addWidget(water_btn)
        else:
            watered_btn = create_styled_button("Watered Today", Styles.SECONDARY_BUTTON, "✅")
            watered_btn.setEnabled(False)
            button_layout.addWidget(watered_btn)

        edit_btn = create_styled_button("Edit", Styles.ACTION_BUTTON, "✏️")
        edit_btn.clicked.connect(lambda: self.show_edit_plant_form(plant))
        button_layout.addWidget(edit_btn)

        delete_btn = create_styled_button("Delete", Styles.DELETE_BUTTON, "🗑️")
        delete_btn.clicked.connect(lambda: self.delete_plant(plant))
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)
        return card

    def get_watering_status(self, plant):
        """Get watering status display info"""
        if self.db.needs_watering(plant):
            return {
                "text": "💧 Needs watering today",
                "style": "color: #d32f2f; font-weight: bold; font-size: 13px;"
            }
        else:
            plant_id, name, date_planted, care_plan, last_watered, created_at = plant
            return {
                "text": f"✅ Watered on {last_watered}",
                "style": "color: #2e7d32; font-weight: bold; font-size: 13px;"
            }

    def water_plant(self, plant_id):
        """Mark plant as watered and refresh display"""
        success = self.db.water_plant(plant_id)
        if success:
            self.show_plant_list()
            QMessageBox.information(self, "Watering", "Plant marked as watered! 💧")

    def show_add_plant_form(self):
        self.clear_layout()
        self.show_plant_form("🌱 Add New Plant", self.save_plant)

    def show_edit_plant_form(self, plant):
        plant_id, name, date_planted, care_plan, last_watered, created_at = plant
        self.editing_plant_id = plant_id
        self.show_plant_form(f"✏️ Edit {name}", self.update_plant, name, date_planted, care_plan)

    def show_plant_form(self, title, save_handler, name="", date_planted="", care=""):
        self.clear_layout()

        # Title
        self.main_layout.addWidget(create_title(title))

        # Form container
        form_frame = create_form_frame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(10)

        # Name field
        self.name_input = create_styled_input("line", "Enter plant name...", name)
        form_layout.addLayout(create_form_section("Plant Name:", self.name_input))

        # Date field - Now using QDateEdit
        date_label = QLabel("Date Planted:")
        date_label.setStyleSheet("font-weight: bold; color: #3e2723; margin-top: 10px;")
        form_layout.addWidget(date_label)

        self.date_input = create_date_edit()
        if date_planted:
            try:
                year, month, day = map(int, date_planted.split('-'))
                self.date_input.setDate(QDate(year, month, day))
            except:
                self.date_input.setDate(QDate.currentDate())
        form_layout.addWidget(self.date_input)

        # Care instructions
        self.care_input = create_styled_input("text", "Water every week, bright indirect light...", care)
        form_layout.addLayout(create_form_section("Care Instructions:", self.care_input))

        self.main_layout.addWidget(form_frame)

        # Buttons
        button_layout = QHBoxLayout()

        save_text = "💾 Save" if "Add" in title else "💾 Update"
        save_btn = create_styled_button(save_text, Styles.PRIMARY_BUTTON)
        save_btn.clicked.connect(save_handler)
        button_layout.addWidget(save_btn)

        back_btn = create_styled_button("Back to Plants", Styles.SECONDARY_BUTTON, "←")
        back_btn.clicked.connect(self.show_plant_list)
        button_layout.addWidget(back_btn)

        self.main_layout.addLayout(button_layout)
        self.name_input.setFocus()

    def save_plant(self):
        name = self.name_input.text().strip()
        date_planted = self.date_input.date().toString("yyyy-MM-dd")
        care_plan = self.care_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Plant name is required!")
            return

        self.db.add_plant(name, date_planted, care_plan)
        self.show_plant_list()

    def update_plant(self):
        if not hasattr(self, 'editing_plant_id'):
            return

        name = self.name_input.text().strip()
        date_planted = self.date_input.date().toString("yyyy-MM-dd")
        care_plan = self.care_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Plant name is required!")
            return

        success = self.db.update_plant(self.editing_plant_id, name, date_planted, care_plan)
        if success:
            self.show_plant_list()

    def show_plant_details(self, plant):
        plant_id, name, date_planted, care_plan, last_watered, created_at = plant
        self.clear_layout()

        # Title
        self.main_layout.addWidget(create_title(f"🌿 {name}"))

        # Plant info
        info_frame = create_form_frame()
        info_layout = QVBoxLayout(info_frame)

        # Watering status in details
        watering_status = self.get_watering_status(plant)
        status_label = QLabel(watering_status["text"])
        status_label.setStyleSheet(watering_status["style"] + " font-size: 16px; padding: 10px;")
        info_layout.addWidget(status_label)

        info_text = f"""
        <div style='font-size: 14px;'>
        <p><b>Planted:</b> {date_planted}</p>
        <p><b>Care Instructions:</b><br>{care_plan if care_plan else 'No care instructions added yet.'}</p>
        </div>
        """
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: #3e2723;")
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)

        # Water button in details
        if self.db.needs_watering(plant):
            water_btn = create_styled_button("Mark as Watered Today", Styles.PRIMARY_BUTTON, "💧")
            water_btn.clicked.connect(lambda: self.water_plant_in_details(plant_id))
            info_layout.addWidget(water_btn)
        else:
            watered_btn = create_styled_button("Already Watered Today", Styles.SECONDARY_BUTTON, "✅")
            watered_btn.setEnabled(False)
            info_layout.addWidget(watered_btn)

        self.main_layout.addWidget(info_frame)

        # Journal entries
        journals_label = QLabel("📖 Journal Entries")
        journals_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3e2723; margin-top: 20px;")
        self.main_layout.addWidget(journals_label)

        # Journal entries list
        entries = self.db.get_journal_entries(plant_id)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        if entries:
            for entry in entries:
                entry_id, entry_plant_id, entry_date, notes, entry_created = entry
                entry_card = self.create_journal_entry_card(entry_id, entry_date, notes, plant_id)
                scroll_layout.addWidget(entry_card)
        else:
            no_entries = QLabel("No journal entries yet. Click 'Add Entry' to start!")
            no_entries.setStyleSheet("color: #8d6e63; font-size: 14px; padding: 20px;")
            no_entries.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scroll_layout.addWidget(no_entries)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll_area, 1)

        # Buttons
        button_layout = QHBoxLayout()

        add_entry_btn = create_styled_button("Add Journal Entry", Styles.PRIMARY_BUTTON, "📝")
        add_entry_btn.clicked.connect(lambda: self.show_add_journal_form(plant_id))
        button_layout.addWidget(add_entry_btn)

        back_btn = create_styled_button("Back to Plants", Styles.SECONDARY_BUTTON, "←")
        back_btn.clicked.connect(self.show_plant_list)
        button_layout.addWidget(back_btn)

        self.main_layout.addLayout(button_layout)

    def water_plant_in_details(self, plant_id):
        """Water plant from details view and refresh details"""
        success = self.db.water_plant(plant_id)
        if success:
            plant = self.db.get_plant_by_id(plant_id)
            self.show_plant_details(plant)
            QMessageBox.information(self, "Watering", "Plant marked as watered! 💧")

    def create_journal_entry_card(self, entry_id, date, notes, plant_id):
        card = create_card_frame()
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # Entry content
        date_label = QLabel(f"<b>📅 Date:</b> {date}")
        date_label.setStyleSheet("font-size: 14px; color: #3e2723; font-weight: bold;")
        layout.addWidget(date_label)

        notes_label = QLabel(f"<b>Notes:</b> {notes}")
        notes_label.setStyleSheet("color: #5d4037; font-size: 13px;")
        notes_label.setWordWrap(True)
        layout.addWidget(notes_label)

        # Action buttons
        button_layout = QHBoxLayout()

        edit_btn = create_styled_button("Edit", Styles.ACTION_BUTTON, "✏️")
        edit_btn.clicked.connect(lambda: self.show_edit_journal_form(entry_id, plant_id))
        button_layout.addWidget(edit_btn)

        delete_btn = create_styled_button("Delete", Styles.DELETE_BUTTON, "🗑️")
        delete_btn.clicked.connect(lambda: self.delete_journal_entry(entry_id, plant_id))
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)
        return card

    def show_add_journal_form(self, plant_id):
        self.clear_layout()
        self.current_journal_plant_id = plant_id

        self.main_layout.addWidget(create_title("📝 Add Journal Entry"))

        # Form container
        form_frame = create_form_frame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)

        # Date field - Using QDateEdit for journal entries too
        date_label = QLabel("Entry Date:")
        date_label.setStyleSheet("font-weight: bold; color: #3e2723;")
        form_layout.addWidget(date_label)

        self.journal_date_input = create_date_edit()
        form_layout.addWidget(self.journal_date_input)

        # Notes field
        self.journal_notes_input = create_styled_input("text", "New leaves growing, looking healthy...")
        self.journal_notes_input.setMinimumHeight(120)
        form_layout.addLayout(create_form_section("Notes:", self.journal_notes_input))

        self.main_layout.addWidget(form_frame)

        # Buttons
        button_layout = QHBoxLayout()

        save_btn = create_styled_button("Save Entry", Styles.PRIMARY_BUTTON, "💾")
        save_btn.clicked.connect(self.save_journal_entry)
        button_layout.addWidget(save_btn)

        back_btn = create_styled_button("Cancel", Styles.SECONDARY_BUTTON, "←")
        plant = self.db.get_plant_by_id(plant_id)
        back_btn.clicked.connect(lambda: self.show_plant_details(plant))
        button_layout.addWidget(back_btn)

        self.main_layout.addLayout(button_layout)
        self.journal_notes_input.setFocus()

    def show_edit_journal_form(self, entry_id, plant_id):
        entries = self.db.get_journal_entries(plant_id)
        entry_data = next((entry for entry in entries if entry[0] == entry_id), None)

        if not entry_data:
            return

        entry_id, entry_plant_id, entry_date, notes, entry_created = entry_data
        self.editing_journal_id = entry_id
        self.current_journal_plant_id = plant_id

        self.clear_layout()
        self.main_layout.addWidget(create_title("✏️ Edit Journal Entry"))

        # Form container
        form_frame = create_form_frame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)

        # Date field - Using QDateEdit
        date_label = QLabel("Entry Date:")
        date_label.setStyleSheet("font-weight: bold; color: #3e2723;")
        form_layout.addWidget(date_label)

        self.journal_date_input = create_date_edit()
        try:
            year, month, day = map(int, entry_date.split('-'))
            self.journal_date_input.setDate(QDate(year, month, day))
        except:
            self.journal_date_input.setDate(QDate.currentDate())
        form_layout.addWidget(self.journal_date_input)

        # Notes field
        self.journal_notes_input = create_styled_input("text", "New leaves growing, looking healthy...", notes)
        self.journal_notes_input.setMinimumHeight(35)
        form_layout.addLayout(create_form_section("Notes:", self.journal_notes_input))

        self.main_layout.addWidget(form_frame)

        # Buttons
        button_layout = QHBoxLayout()

        save_btn = create_styled_button("Update Entry", Styles.PRIMARY_BUTTON, "💾")
        save_btn.clicked.connect(self.update_journal_entry)
        button_layout.addWidget(save_btn)

        back_btn = create_styled_button("Cancel", Styles.SECONDARY_BUTTON, "←")
        plant = self.db.get_plant_by_id(plant_id)
        back_btn.clicked.connect(lambda: self.show_plant_details(plant))
        button_layout.addWidget(back_btn)

        self.main_layout.addLayout(button_layout)
        self.journal_notes_input.setFocus()

    def update_journal_entry(self):
        if not hasattr(self, 'editing_journal_id'):
            return

        entry_date = self.journal_date_input.date().toString("yyyy-MM-dd")
        notes = self.journal_notes_input.toPlainText().strip()

        if not entry_date or not notes:
            QMessageBox.warning(self, "Input Error", "Both date and notes are required!")
            return

        success = self.db.update_journal_entry(self.editing_journal_id, entry_date, notes)
        if success:
            plant = self.db.get_plant_by_id(self.current_journal_plant_id)
            self.show_plant_details(plant)

    def delete_journal_entry(self, entry_id, plant_id):
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this journal entry?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_journal_entry(entry_id)
            plant = self.db.get_plant_by_id(plant_id)
            self.show_plant_details(plant)

    def save_journal_entry(self):
        if not hasattr(self, 'current_journal_plant_id'):
            return

        entry_date = self.journal_date_input.date().toString("yyyy-MM-dd")
        notes = self.journal_notes_input.toPlainText().strip()

        if not entry_date or not notes:
            QMessageBox.warning(self, "Input Error", "Both date and notes are required!")
            return

        self.db.add_journal_entry(self.current_journal_plant_id, entry_date, notes)
        plant = self.db.get_plant_by_id(self.current_journal_plant_id)
        self.show_plant_details(plant)

    def delete_plant(self, plant):
        plant_id, name, date_planted, care_plan, last_watered, created_at = plant

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Are you sure you want to delete "{name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = self.db.delete_plant(plant_id)
            if success:
                self.show_plant_list()

    def clear_layout(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
