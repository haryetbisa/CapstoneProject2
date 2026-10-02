# screens/student_progress.py
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
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PySide6.QtGui import QIcon

from themes.colors import *
from themes.fonts import BODY_FONT, HEADING_FONT
from session import AppSession
from Database.queries import get_student_activity_logs

ICONS_DIR = os.path.join(ROOT_DIR, "assets", "icons")

class StudentProgressScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # Top Bar
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: none;")
        back_btn.clicked.connect(lambda: self.router.navigate("kindergarten"))
        top_layout.addWidget(back_btn)

        self.title_label = QLabel("Ulat ng Mag-aaral (Student Progress)")
        self.title_label.setStyleSheet(f"font-family: {HEADING_FONT}; color: {CHOCO_BROWN}; font-size: 24px;")
        top_layout.addWidget(self.title_label)

        # Table for Logs
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Module", "Target Word", "Score", "Accuracy", "Date / Time"])
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
        self.load_progress_logs()

    def load_progress_logs(self):
        """Loads activity logs for the currently active student in session."""
        self.table.setRowCount(0)
        student_id = AppSession.get_active_student_id()
        student_name = AppSession.get_student_name()

        if not student_id:
            QMessageBox.warning(self, "Babala", "Walang napiling mag-aaral. Pumili muna sa dashboard.")
            return

        self.title_label.setText(f"Ulat ng Mag-aaral: {student_name}")
        logs = get_student_activity_logs(student_id)

        for row_idx, log in enumerate(logs):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(log.get('module_name', ''))))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(log.get('target_word') or 'N/A')))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(log.get('score', '0'))))
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{log.get('speech_accuracy', 0)}%" if log.get('speech_accuracy') else 'N/A'))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(log.get('timestamp', ''))))