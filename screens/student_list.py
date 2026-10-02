# screens/student_list.py
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PySide6.QtGui import QIcon

from themes.colors import *
from themes.fonts import BODY_FONT, HEADING_FONT
from session import AppSession
from Database.queries import get_students_by_teacher, add_student

ICONS_DIR = os.path.join(ROOT_DIR, "assets", "icons")

class StudentListScreen(QWidget):
    def __init__(self, router, section_name="Kindergarten - Paharang"):
        super().__init__()
        self.router = router
        self.section_name = section_name

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # Top Navigation & Title Bar
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: none;")
        back_btn.clicked.connect(self.go_back)
        top_layout.addWidget(back_btn)

        title = QLabel(f"Student Roster - {self.section_name}")
        title.setStyleSheet(f"font-family: {HEADING_FONT}; color: {CHOCO_BROWN}; font-size: 24px;")
        top_layout.addWidget(title)

        # Add Student Input Form Layout
        form_layout = QHBoxLayout()
        
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setStyleSheet(self.input_stylesheet())
        
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setStyleSheet(self.input_stylesheet())

        self.add_btn = QPushButton("Add Student")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 15px;
                font-weight: 700;
                border-radius: 6px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.add_btn.clicked.connect(self.handle_add_student)

        form_layout.addWidget(self.first_name_input, 2)
        form_layout.addWidget(self.last_name_input, 2)
        form_layout.addWidget(self.add_btn, 1)
        main_layout.addLayout(form_layout)

        # Student Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["First Name", "Last Name", "Grade & Section"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {LIGHT};
                border: 2px solid {CORAL_RED};
                border-radius: 6px;
                font-family: {BODY_FONT};
                font-size: 15px;
                color: {CHOCO_BROWN};
            }}
            QHeaderView::section {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-weight: bold;
                padding: 8px;
                border: none;
            }}
        """)
        main_layout.addWidget(self.table)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_students()

    def go_back(self):
        """Dynamically returns to the correct level dashboard based on section name."""
        if "Grade 1" in self.section_name:
            self.router.navigate("grade1_dash")
        else:
            self.router.navigate("kindergarten")

    def input_stylesheet(self):
        return f"""
            QLineEdit {{
                font-family: {BODY_FONT};
                font-size: 15px;
                color: {CHOCO_BROWN};
                border: 2px solid {CORAL_RED};
                border-radius: 6px;
                background-color: {LIGHT};
                padding: 8px 14px;
            }}
        """

    def load_students(self):
        """Loads student data from local SQLite database for the active teacher."""
        self.table.setRowCount(0)
        teacher_id = AppSession.get_teacher_id()
        
        if not teacher_id:
            return

        students = get_students_by_teacher(teacher_id)
        for row_idx, student in enumerate(students):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(student['first_name']))
            self.table.setItem(row_idx, 1, QTableWidgetItem(student['last_name']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(student['grade_section']))

    def handle_add_student(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        teacher_id = AppSession.get_teacher_id()

        if not teacher_id:
            QMessageBox.warning(self, "Error", "No active teacher session found. Please log in again.")
            return

        if not first_name or not last_name:
            QMessageBox.warning(self, "Validation Error", "Please provide both first and last name.")
            return

        try:
            add_student(teacher_id=teacher_id, first_name=first_name, last_name=last_name, section=self.section_name)
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.load_students()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to add student: {str(e)}")