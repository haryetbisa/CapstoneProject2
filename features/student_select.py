# features/student_select.py
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt

from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT
from session import AppSession
from Database.queries import get_students_by_teacher

class StudentSelect(QDialog):
    def __init__(self, parent=None, module_name="Module"):
        super().__init__(parent)
        self.module_name = module_name
        self.selected_student = None

        self.setWindowTitle("Pumili ng Mag-aaral")
        self.resize(420, 500)
        self.setStyleSheet(f"background-color: {LIGHT};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel(f"Pumili ng Mag-aaral para sa {self.module_name}")
        title.setStyleSheet(f"font-family: {HEADING_FONT}; color: {CHOCO_BROWN}; font-size: 18px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Student List Widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: #FFFBF0;
                border: 2px solid {CORAL_RED};
                border-radius: 8px;
                font-family: {BODY_FONT};
                font-size: 16px;
                color: {CHOCO_BROWN};
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid #EFE8DA;
            }}
            QListWidget::item:selected {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.list_widget)
        self.load_students()

        # Start Button
        self.select_btn = QPushButton("Simulan ang Laro")
        self.select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 16px;
                font-weight: 700;
                border-radius: 6px;
                padding: 12px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.select_btn.clicked.connect(self.confirm_selection)
        layout.addWidget(self.select_btn)

    def load_students(self):
        """Fetches students from the local database for the logged-in teacher."""
        teacher_id = AppSession.get_teacher_id()
        if not teacher_id:
            return

        students = get_students_by_teacher(teacher_id)
        for s in students:
            full_name = f"{s['first_name']} {s['last_name']} ({s['grade_section']})"
            item = QListWidgetItem(full_name)
            item.setData(Qt.ItemDataRole.UserRole, s)
            self.list_widget.addItem(item)

    def confirm_selection(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Babala", "Mangyaring pumili muna ng mag-aaral sa listahan.")
            return
        
        self.selected_student = selected_items[0].data(Qt.ItemDataRole.UserRole)
        self.accept()