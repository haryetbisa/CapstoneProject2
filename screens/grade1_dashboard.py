
# screens/grade1_dashboard.py
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from components.cardsbutton import CardsButton
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT
from session import AppSession
from Database.queries import get_students_by_teacher

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")
BGM_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds", "bgm")
BGM_FILE = "clappy-ukulele.mp3"

class GradeOneDashboard(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(60, 60, 60, 0)
        
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

        title = QLabel("GRADE 1 DASHBOARD")
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
        self.roster_btn.clicked.connect(lambda: self.router.navigate("grade1_roster"))
        top_layout.addWidget(self.roster_btn)

        main_layout.addSpacing(40)
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)     
        grid_layout.setContentsMargins(0, 50, 0, 0)

        bilang_card = CardsButton("Bilang", "Bilang.png", color = LIGHT_GREEN)
        bilang_card.clicked.connect(lambda: self.navigate_with_validation("bilang_g1"))

        salita = CardsButton("Salita", "Pangungusap.png", color = MAGENTA)
        salita.clicked.connect(lambda: self.navigate_with_validation("salita"))

        kuwento_card = CardsButton("Kuwento", "kuwento.png", color = ORCHID_PINK)
        kuwento_card.clicked.connect(lambda: self.navigate_with_validation("kuwento"))
        
        grid_layout.addWidget(bilang_card, 0, 0)
        grid_layout.addWidget(salita, 0, 1)
        grid_layout.addWidget(kuwento_card, 0, 2)
      
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

    def showEvent(self, event):
        self.load_dropdown_students()
        self.play_instruction_sound()
        super().showEvent(event)

    def stop_instruction_sound(self):
        self.instruction_player.stop()

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def play_instruction_sound(self):
        sound_path = os.path.abspath(os.path.join(BGM_DIR, BGM_FILE))
        if os.path.exists(sound_path):
            self.instruction_player.stop()
            self.instruction_player.setSource(QUrl.fromLocalFile(sound_path))
            self.instruction_player.play()
        else:
            print(f"Instruction sound not found: {sound_path}")

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
            print(f"--> Grade 1 Active Student Set to ID: {student_id}")

    def navigate_with_validation(self, route_name):
        student_id = AppSession.get_active_student_id()
        if not student_id:
            QMessageBox.warning(self, "Babala", "Mangyaring pumili muna ng mag-aaral mula sa dropdown bago simulan ang laro.")
            return
        self.router.navigate(route_name)

