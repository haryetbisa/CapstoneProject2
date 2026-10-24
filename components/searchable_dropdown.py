# components/searchable_dropdown.py
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QFrame
)
from themes.colors import *
from themes.fonts import BODY_FONT

class SearchableDropdown(QWidget):
    studentSelected = Signal(str, str)  

    def __init__(self, placeholder="-- Pumili ng Mag-aaral --", parent=None):
        super().__init__(parent)
        self.selected_student_id = None
        self.students_data = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Main Button acting as the dropdown header
        self.main_btn = QPushButton(placeholder)
        self.main_btn.setCursor(Qt.PointingHandCursor)
        self.main_btn.setMinimumWidth(240)
        self.main_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {BODY_FONT};
                font-size: 14px;
                color: {CHOCO_BROWN};
                background-color: {LIGHT};
                border: 2px solid {CORAL_RED};
                border-radius: 6px;
                padding: 6px 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: #faf5ee;
            }}
        """)
        self.main_btn.clicked.connect(self.toggle_popup)
        layout.addWidget(self.main_btn)

        # Popup Panel Container (Frame with Search + List)
        self.popup = QFrame(self, Qt.Popup)
        self.popup.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT};
                border: 2px solid {CORAL_RED};
                border-radius: 6px;
            }}
        """)
        
        popup_layout = QVBoxLayout(self.popup)
        popup_layout.setContentsMargins(6, 6, 6, 6)
        popup_layout.setSpacing(6)

        # Search Bar Inside Popup
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {BODY_FONT};
                font-size: 13px;
                color: {CHOCO_BROWN};
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 5px;
            }}
        """)
        self.search_input.textChanged.connect(self.filter_students)
        popup_layout.addWidget(self.search_input)

        # List Widget for Students
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                font-family: {BODY_FONT};
                font-size: 14px;
                color: {CHOCO_BROWN};
                background-color: {LIGHT};
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                padding: 6px;
                border-radius: 4px;
            }}
            QListWidget::item:hover {{
                background-color: {CORAL_RED};
                color: {LIGHT};
            }}
        """)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        popup_layout.addWidget(self.list_widget)
        
        self.popup.hide()

    def set_students(self, students):
        self.students_data = students
        self.populate_list(students)

    def populate_list(self, students):
        self.list_widget.clear()
        
        default_item = QListWidgetItem("-- Pumili ng Mag-aaral --")
        default_item.setData(Qt.UserRole, None)
        self.list_widget.addItem(default_item)

        for s in students:
            item = QListWidgetItem(s["full_name"])
            item.setData(Qt.UserRole, s["student_id"])
            self.list_widget.addItem(item)

    def filter_students(self, query):
        query = query.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if i == 0:
                continue
            matches = query in item.text().lower()
            item.setHidden(not matches)

    def toggle_popup(self):
        if self.popup.isVisible():
            self.popup.hide()
        else:
            btn_pos = self.main_btn.mapToGlobal(QPoint(0, self.main_btn.height()))
            self.popup.setGeometry(btn_pos.x(), btn_pos.y(), self.main_btn.width(), 200)
            self.search_input.clear()
            self.filter_students("")
            self.popup.show()
            self.search_input.setFocus()

    def on_item_clicked(self, item):
        student_id = item.data(Qt.UserRole)
        full_name = item.text()
        
        if student_id is None:
            self.main_btn.setText("-- Pumili ng Mag-aaral --")
        else:
            self.main_btn.setText(full_name)
            
        self.selected_student_id = student_id
        self.popup.hide()
        self.studentSelected.emit(str(student_id) if student_id else "", full_name)

    def set_selected_student(self, student_id, full_name):
        self.selected_student_id = student_id
        self.main_btn.setText(full_name if full_name else "-- Pumili ng Mag-aaral --")