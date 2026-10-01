# components/top_navbar.py

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QFrame
)
from themes.colors import *
from themes.fonts import BODY_FONT

from Database.queries import get_students_by_teacher, add_student
from session import AppSession


class TopNavbar(QFrame):
    """Global navigation bar containing teacher info, active student selector, and logout."""

    student_changed = Signal(str)  # Emits student_id when active pupil is switched

    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self.students_map = {}  # Maps display string -> student_id

        self.setFixedHeight(64)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT};
                border-bottom: 2px solid {CORAL_RED};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(15)

        # 1. App Title / Home Button
        self.home_btn = QPushButton("BasaMatika")
        self.home_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.home_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {BODY_FONT};
                font-size: 20px;
                font-weight: 900;
                color: {CORAL_RED};
                background: transparent;
                border: none;
            }}
            QPushButton:hover {{
                color: #d94338;
            }}
        """)
        self.home_btn.clicked.connect(lambda: self.router.navigate("home"))
        layout.addWidget(self.home_btn)

        layout.addStretch()

        # 2. Student Selector Label & Dropdown
        student_label = QLabel("Pumili ng Mag-aaral:")
        student_label.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 15px; color: {CHOCO_BROWN}; font-weight: 600; border: none;")
        layout.addWidget(student_label)

        self.student_combo = QComboBox()
        self.student_combo.setFixedWidth(240)
        self.student_combo.setStyleSheet(f"""
            QComboBox {{
                font-family: {BODY_FONT};
                font-size: 14px;
                color: {CHOCO_BROWN};
                border: 1.5px solid {CORAL_RED};
                border-radius: 6px;
                padding: 4px 8px;
                background-color: white;
            }}
        """)
        self.student_combo.currentIndexChanged.connect(self.on_student_selected)
        layout.addWidget(self.student_combo)

        # 3. Add Student Quick Button
        self.add_student_btn = QPushButton("+ Magdagdag")
        self.add_student_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_student_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 13px;
                font-weight: 700;
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.add_student_btn.clicked.connect(self.prompt_add_student)
        layout.addWidget(self.add_student_btn)

        # Separator Line
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep)

        # 4. Teacher Profile Badge
        self.teacher_label = QLabel("Guro: Walang Login")
        self.teacher_label.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 14px; color: {CHOCO_BROWN}; font-weight: 600; border: none;")
        layout.addWidget(self.teacher_label)

        # 5. Logout Button
        self.logout_btn = QPushButton("Lumabas")
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.setStyleSheet(f"""
            QPushButton {{
                font-family: {BODY_FONT};
                font-size: 13px;
                color: #d93025;
                background: transparent;
                border: 1px solid #d93025;
                border-radius: 4px;
                padding: 4px 10px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #fce8e6;
            }}
        """)
        self.logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(self.logout_btn)

        # Load initial session data
        self.refresh_navbar()

    def refresh_navbar(self):
        """Reloads active teacher display name and pupil roster dropdown."""
        # Update Teacher Label
        if AppSession.is_teacher_logged_in():
            self.teacher_label.setText(f"Guro: {AppSession.get_teacher_name()}")
            self.load_students_for_teacher(AppSession.get_teacher_id())
        else:
            self.teacher_label.setText("Guro: Walang Login")
            self.student_combo.clear()

    def load_students_for_teacher(self, teacher_id: str):
        """Fetches pupils from local SQLite database and populates dropdown."""
        self.student_combo.blockSignals(True)
        self.student_combo.clear()
        self.students_map.clear()

        students = get_students_by_teacher(teacher_id)

        if not students:
            self.student_combo.addItem("-- Walang Mag-aaral --", None)
            AppSession.clear_student()
        else:
            for s in students:
                display_name = f"{s['last_name']}, {s['first_name']}"
                self.students_map[display_name] = s['student_id']
                self.student_combo.addItem(display_name, s['student_id'])

            # Set first student as active session by default
            first_name = self.student_combo.currentText()
            first_id = self.students_map.get(first_name)
            if first_id:
                AppSession.set_student(first_id, first_name)

        self.student_combo.blockSignals(False)

    def on_student_selected(self, index: int):
        """Fired when teacher selects a different student in the dropdown."""
        selected_text = self.student_combo.currentText()
        student_id = self.students_map.get(selected_text)

        if student_id:
            AppSession.set_student(student_id, selected_text)
            self.student_changed.emit(student_id)
            print(f"--> Active Student set to: {selected_text} ({student_id})")

    def prompt_add_student(self):
        """Shows a popup dialog to quickly register a student under the active teacher."""
        from PySide6.QtWidgets import QInputDialog, QMessageBox

        if not AppSession.is_teacher_logged_in():
            QMessageBox.warning(self, "Kamalian", "Paki-login muna ang guro bago magdagdag ng mag-aaral.")
            return

        name, ok = QInputDialog.getText(self, "Bagong Mag-aaral", "Ipasok ang Buong Pangalan (hal. Juan Dela Cruz):")
        if ok and name.strip():
            parts = name.strip().split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

            student_id = add_student(
                teacher_id=AppSession.get_teacher_id(),
                first_name=first_name,
                last_name=last_name,
                section="Kindergarten - Paharang"
            )

            print(f"--> Added new student: {name} ({student_id})")
            self.refresh_navbar()

    def handle_logout(self):
        """Clears global session and redirects back to account registration/login screen."""
        AppSession.clear_all()
        print("--> Teacher logged out.")
        self.router.navigate("account_info")