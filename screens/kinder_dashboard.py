# screens/kinder_dashboard.py
import os
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QMessageBox
from PySide6.QtGui import QIcon

from components.cardsbutton import CardsButton
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT
from session import AppSession
from Database.queries import get_students_by_teacher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


class KinderDashboard(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: none; border-radius: 6px;")
        back_btn.clicked.connect(lambda: self.router.navigate("home"))
        top_layout.addWidget(back_btn)

        title = QLabel("KINDERGARTEN DASHBOARD")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 32px;
            font-family: {HEADING_FONT};
            font-weight: 900;
            color: {CHOCO_BROWN};
        """)
        top_layout.addWidget(title)
        top_layout.setSpacing(30)

        # Student Dropdown Selector with Fixed Popup Styling
        self.student_combo = QComboBox()
        self.student_combo.setMinimumWidth(220)
        self.student_combo.setCursor(Qt.PointingHandCursor)
        self.student_combo.setStyleSheet(f"""
            QComboBox {{
                font-family: {BODY_FONT};
                font-size: 14px;
                color: {CHOCO_BROWN};
                background-color: {LIGHT};
                border: 2px solid {CORAL_RED};
                border-radius: 6px;
                padding: 6px 12px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {LIGHT};
                color: {CHOCO_BROWN};
                selection-background-color: {CORAL_RED};
                selection-color: {LIGHT};
                border: 2px solid {CORAL_RED};
                outline: none;
                padding: 4px;
            }}
        """)
        self.student_combo.currentIndexChanged.connect(self.on_student_changed)
        top_layout.addWidget(self.student_combo)

        self.roster_btn = QPushButton("Mag-aaral (listahan)")
        self.roster_btn.setCursor(Qt.PointingHandCursor)
        self.roster_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 14px;
                font-weight: 700;
                border-radius: 6px;
                padding: 10px 16px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.roster_btn.clicked.connect(lambda: self.router.navigate("kindergarten_roster"))
        top_layout.addWidget(self.roster_btn)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(50)        
        grid_layout.setContentsMargins(0, 50, 0, 0)

        pantig_card = CardsButton("Pantig", "pantig.png", color = LIGHT_GREEN)
        pantig_card.clicked.connect(lambda: self.navigate_with_validation("pantig"))

        bilang_card = CardsButton("Bilang", "Bilang.png", color = MAGENTA)
        bilang_card.clicked.connect(lambda: self.navigate_with_validation("bilang"))

        hugis_card = CardsButton("Hugis", "hugis.png", color = ORCHID_PINK) 
        hugis_card.clicked.connect(lambda: self.navigate_with_validation("hugis"))

        parte_card = CardsButton("Parte ng Katawan", "parte.png", color = SKY_BLUE)
        parte_card.clicked.connect(lambda: self.navigate_with_validation("katawan"))

        kulay_card = CardsButton("Kulay", "kulay.png", color = LIGHT_CORAL_PINK) 
        kulay_card.clicked.connect(lambda: self.navigate_with_validation("kulay"))

        hayop_card = CardsButton("Hayop", "hayop.png", color = COBALT_BLUE) 
        hayop_card.clicked.connect(lambda: self.navigate_with_validation("hayop"))

        grid_layout.addWidget(pantig_card, 0, 0)
        grid_layout.addWidget(bilang_card, 0, 1)
        grid_layout.addWidget(hugis_card, 0, 2)
        grid_layout.addWidget(parte_card, 1, 0)
        grid_layout.addWidget(kulay_card, 1, 1)
        grid_layout.addWidget(hayop_card, 1, 2)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_dropdown_students()

    def load_dropdown_students(self):
        """Populates the dropdown with students belonging to the active teacher."""
        self.student_combo.blockSignals(True)
        self.student_combo.clear()
        self.student_combo.addItem("-- Pumili ng Mag-aaral --", None)

        teacher_id = AppSession.get_teacher_id()
        if teacher_id:
            students = get_students_by_teacher(teacher_id)
            for s in students:
                full_name = f"{s['first_name']} {s['last_name']}"
                self.student_combo.addItem(full_name, str(s['student_id']))

        current_id = AppSession.get_active_student_id()
        if current_id:
            index = self.student_combo.findData(str(current_id))
            if index != -1:
                self.student_combo.setCurrentIndex(index)

        self.student_combo.blockSignals(False)

    def on_student_changed(self, index):
        if index <= 0:
            AppSession.set_active_student_id(None)
            return
        student_id = self.student_combo.currentData()
        AppSession.set_active_student_id(student_id)
        if student_id:
            print(f"--> Active Student Set to ID: {student_id}")

    def navigate_with_validation(self, route_name):
        student_id = AppSession.get_active_student_id()
        if not student_id:
            QMessageBox.warning(self, "Babala", "Mangyaring pumili muna ng mag-aaral mula sa dropdown bago simulan ang laro.")
            return
        self.router.navigate(route_name)