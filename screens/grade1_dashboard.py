from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from components.cardsbutton import CardsButton
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")
BGM_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds", "bgm")
BGM_FILE = "clappy-ukulele.mp3"


class GradeOneDashboard(QWidget):
    def __init__(self,router):
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
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("home"))
        main_layout.setAlignment(back_btn, Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(back_btn)

        title = QLabel("GRADE 1 DASHBOARD")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 40px;
            font-family: {HEADING_FONT};
            font-weight: 900;
            color: {CHOCO_BROWN};
        """)
        top_layout.addWidget(title)
        top_layout.setSpacing(130)
        main_layout.addLayout(top_layout)

        main_layout.addSpacing(40)
        grid_layout =QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)     
        grid_layout.setContentsMargins(0, 50, 0, 0)

        bilang_card = CardsButton("Bilang", "Bilang.png", color = LIGHT_GREEN)
        bilang_card.clicked.connect(lambda: self.router.navigate("bilang_g1"))

        salita = CardsButton("Salita", "Pangungusap.png", color = MAGENTA)
        salita.clicked.connect(lambda: self.router.navigate("salita"))

        kuwento_card = CardsButton("Kuwento", "kuwento.png", color = ORCHID_PINK)
        kuwento_card.clicked.connect(lambda: self.router.navigate("kuwento"))
        
        grid_layout.addWidget(bilang_card, 0, 0)
        grid_layout.addWidget(salita, 0, 1)
        grid_layout.addWidget(kuwento_card, 0, 2)
      

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

    def showEvent(self, event):
        self.play_instruction_sound()
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
        else:
            print(f"Instruction sound not found: {sound_path}")

    def stop_instruction_sound(self):
        self.instruction_player.stop()

