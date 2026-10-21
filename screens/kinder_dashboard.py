# screens/kinder_dashboard.py
import os

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")
BGM_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds", "bgm")
BGM_FILE = "clappy-ukulele.mp3"


class KinderDashboard(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

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
        self.roster_btn.clicked.connect(lambda: self.router.navigate("kindergarten_roster"))
        top_layout.addWidget(self.roster_btn)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(50)        
        grid_layout.setContentsMargins(0, 50, 0, 0)

        # Initialize Card Buttons and keep references for updating progress
        self.pantig_card = CardsButton("Pantig", "pantig.png", color = LIGHT_GREEN)
        self.pantig_card.clicked.connect(lambda: self.navigate_with_validation("pantig"))

        self.bilang_card = CardsButton("Bilang", "Bilang.png", color = MAGENTA)
        self.bilang_card.clicked.connect(lambda: self.navigate_with_validation("bilang"))

        self.hugis_card = CardsButton("Hugis", "hugis.png", color = ORCHID_PINK) 
        self.hugis_card.clicked.connect(lambda: self.navigate_with_validation("hugis"))

        self.parte_card = CardsButton("Parte ng Katawan", "parte.png", color = SKY_BLUE)
        self.parte_card.clicked.connect(lambda: self.navigate_with_validation("katawan"))

        self.kulay_card = CardsButton("Kulay", "kulay.png", color = LIGHT_CORAL_PINK) 
        self.kulay_card.clicked.connect(lambda: self.navigate_with_validation("kulay"))

        self.hayop_card = CardsButton("Hayop", "hayop.png", color = COBALT_BLUE) 
        self.hayop_card.clicked.connect(lambda: self.navigate_with_validation("hayop"))

        grid_layout.addWidget(self.pantig_card, 0, 0)
        grid_layout.addWidget(self.bilang_card, 0, 1)
        grid_layout.addWidget(self.hugis_card, 0, 2)
        grid_layout.addWidget(self.parte_card, 1, 0)
        grid_layout.addWidget(self.kulay_card, 1, 1)
        grid_layout.addWidget(self.hayop_card, 1, 2)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

    def showEvent(self, event):
        self.play_instruction_sound()
        self.load_dropdown_students()
        self.refresh_progress_bars()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def play_instruction_sound(self):
        sound_path = os.path.abspath(os.path.join(BGM_DIR, BGM_FILE))
        if os.path.exists(sound_path):
            self.instruction_player.stop()
            self.instruction_player.setSource(QUrl.fromLocalFile(sound_path))
            self.instruction_player.play()

    def stop_instruction_sound(self):
        self.instruction_player.stop()

    def load_dropdown_students(self):
        """Populates the dropdown with only Kindergarten students."""
        teacher_id = AppSession.get_teacher_id()
        students_list = []
        active_name = ""

        if teacher_id:
            students = get_students_by_teacher_and_section(teacher_id, "Kindergarten - Paharang")
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
        """Fetches and updates progress percentages for the active student across all modules."""
        student_id = AppSession.get_active_student_id()
        
        # Calculate progress for each module (adjust total_module_items as needed based on your total sub-lessons)
        pantig_pct = get_module_progress_percentage(student_id, "Pantig", total_module_items=15)
        bilang_pct = get_module_progress_percentage(student_id, "Bilang", total_module_items=10)
        hugis_pct = get_module_progress_percentage(student_id, "Hugis", total_module_items=10)
        parte_pct = get_module_progress_percentage(student_id, "Parte ng Katawan", total_module_items=10)
        kulay_pct = get_module_progress_percentage(student_id, "Kulay", total_module_items=10)
        hayop_pct = get_module_progress_percentage(student_id, "Hayop", total_module_items=10)

        # Apply to cards
        self.pantig_card.set_progress(pantig_pct)
        self.bilang_card.set_progress(bilang_pct)
        self.hugis_card.set_progress(hugis_pct)
        self.parte_card.set_progress(parte_pct)
        self.kulay_card.set_progress(kulay_pct)
        self.hayop_card.set_progress(hayop_pct)

    def on_student_selected(self, student_id, full_name):
        if not student_id:
            AppSession.set_active_student_id(None)
            print("--> Active Student Cleared.")
        else:
            AppSession.set_active_student_id(student_id)
            print(f"--> Active Student Set to ID: {student_id} ({full_name})")
        
        # Refresh progress bars immediately when a new student is picked
        self.refresh_progress_bars()

    def navigate_with_validation(self, route_name):
        student_id = AppSession.get_active_student_id()
        if not student_id:
            QMessageBox.warning(self, "Babala", "Mangyaring pumili muna ng mag-aaral mula sa listahan bago simulan ang laro.")
            return
        self.router.navigate(route_name)