# screens/grade1_dashboard.py
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from components.cardsbutton import CardsButton
from components.searchable_dropdown import SearchableDropdown
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT
from session import AppSession
from Database.queries import get_students_by_teacher_and_section, get_module_progress_percentage

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
        self.instruction_player.setLoops(QMediaPlayer.Infinite)  # Loop BGM automatically

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(60, 60, 60, 0)
        
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # Custom Searchable Dropdown
        self.student_dropdown = SearchableDropdown(placeholder="-- Pumili ng Mag-aaral --")
        self.student_dropdown.studentSelected.connect(self.on_student_selected)
        top_layout.addWidget(self.student_dropdown)

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

        # Initialize Grade 1 Cards
        self.bilang_card = CardsButton("Bilang", "Bilang.png", color = LIGHT_GREEN)
        self.bilang_card.clicked.connect(lambda: self.navigate_with_validation("bilang_g1"))

        self.salita_card = CardsButton("Salita", "Pangungusap.png", color = MAGENTA)
        self.salita_card.clicked.connect(lambda: self.navigate_with_validation("salita"))

        self.kuwento_card = CardsButton("Kuwento", "kuwento.png", color = ORCHID_PINK)
        self.kuwento_card.clicked.connect(lambda: self.navigate_with_validation("kuwento"))
        
        grid_layout.addWidget(self.bilang_card, 0, 0)
        grid_layout.addWidget(self.salita_card, 0, 1)
        grid_layout.addWidget(self.kuwento_card, 0, 2)
      
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

    def showEvent(self, event):
        self.play_instruction_sound()
        self.load_dropdown_students()
        self.refresh_progress_bars()
        super().showEvent(event)

    def stop_instruction_sound(self):
        if self.instruction_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.instruction_player.stop()

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def play_instruction_sound(self):
        sound_path = os.path.abspath(os.path.join(BGM_DIR, BGM_FILE))
        if os.path.exists(sound_path):
            current_vol = AppSession.get_music_volume() if hasattr(AppSession, 'get_music_volume') else 0.7
            self.instruction_audio_output.setVolume(current_vol)

            self.instruction_player.stop()
            self.instruction_player.setSource(QUrl.fromLocalFile(sound_path))
            self.instruction_player.play()

    def load_dropdown_students(self):
        """Populates the dropdown with only Grade 1 students."""
        teacher_id = AppSession.get_teacher_id()
        students_list = []
        active_name = ""

        if teacher_id:
            students = get_students_by_teacher_and_section(teacher_id, "Grade 1 - Paharang")
            for s in students:
                full_name = f"{s['first_name']} {s['last_name']}"
                sid = str(s['student_id'])
                students_list.append({"student_id": sid, "full_name": full_name})

                if sid == str(AppSession.get_active_student_id()):
                    active_name = full_name

        self.student_dropdown.set_students(students_list)
        if active_name:
            self.student_dropdown.set_selected_student(AppSession.get_active_student_id(), active_name)
        else:
            self.student_dropdown.set_selected_student(None, "")

    def refresh_progress_bars(self):
        """Fetches and updates progress percentages for the active student in Grade 1."""
        student_id = AppSession.get_active_student_id()
        
        bilang_pct = get_module_progress_percentage(student_id, "Bilang (G1)", total_module_items=10)
        salita_pct = get_module_progress_percentage(student_id, "Salita", total_module_items=10)
        kuwento_pct = get_module_progress_percentage(student_id, "Kuwento", total_module_items=5)

        self.bilang_card.set_progress(bilang_pct)
        self.salita_card.set_progress(salita_pct)
        self.kuwento_card.set_progress(kuwento_pct)

    def on_student_selected(self, student_id, full_name):
        if not student_id:
            AppSession.set_active_student_id(None)
            print("--> Grade 1 Active Student Cleared.")
        else:
            AppSession.set_active_student_id(student_id)
            print(f"--> Grade 1 Active Student Set to ID: {student_id} ({full_name})")
        
        self.refresh_progress_bars()

    def navigate_with_validation(self, route_name):
        student_id = AppSession.get_active_student_id()
        if not student_id:
            QMessageBox.warning(self, "Babala", "Mangyaring pumili muna ng mag-aaral mula sa listahan bago simulan ang laro.")
            return
        self.router.navigate(route_name)