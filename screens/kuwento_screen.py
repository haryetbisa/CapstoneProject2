from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from themes.fonts import HEADING_FONT, BODY_FONT

from components.cardsg1 import CardsButtonG1
from themes.colors import *

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "kuwento")
ICONS_DIR = os.path.join(BASE_DIR, "..","assets", "icons")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds", "bgm")
INSTRUCTION_SOUND_FILE = "Up-on-a-Housetop.mp3"



class KuwentoScreen(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60,60,60,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("grade1_dash"))

   
        pagsasanay = QLabel("Kuwento")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(20)


        grid_layout =QGridLayout()
        grid_layout.setSpacing(50)        
        grid_layout.setContentsMargins(0, 50, 0, 0)


        lvl1 = CardsButtonG1("Ang Malusog na Bata", "AMNB.png", color = CORAL_RED)
        lvl1.clicked.connect(lambda: self.router.navigate("level1"))

        lvl2 = CardsButtonG1("Ang Aking Alaga", "AAA.png", color = MARIGOLD)
        lvl2.clicked.connect(lambda: self.router.navigate("level2"))

        lvl3 = CardsButtonG1("Ang Ating Bandila", "AAB.png", color = ELECTRIC_VIOLET)
        lvl3.clicked.connect(lambda: self.router.navigate("level3"))

        lvl4 = CardsButtonG1("Ang Saranggola", "AS.png", color = HOT_PINK)
        lvl4.clicked.connect(lambda: self.router.navigate("level4"))

        lvl5 = CardsButtonG1("Sa Halamanan", "SH.png", color = SKY_BLUE)
        lvl5.clicked.connect(lambda: self.router.navigate("level5"))

        lvl6 = CardsButtonG1("Ang Lapis ni Dan", "ALD.png", color = LIGHT_GREEN)
        lvl6.clicked.connect(lambda: self.router.navigate("level6"))

        lvl7 = CardsButtonG1("Ang Libro", "AL.png", color = COBALT_BLUE)
        lvl7.clicked.connect(lambda: self.router.navigate("level7"))
        
        lvl8 = CardsButtonG1("Mang Dada", "MD.png", color = TERRACOTTA )
        lvl8.clicked.connect(lambda: self.router.navigate("level8"))

        lvl9 = CardsButtonG1("Ang Po at Opo", "APAO.png", color = DARK_YELLOW )
        lvl9.clicked.connect(lambda: self.router.navigate("level9"))

        lvl10 = CardsButtonG1("Ang Batang Munti", "ABM.png", color = MAGENTA )
        lvl10.clicked.connect(lambda: self.router.navigate("level10"))

        
        grid_layout.addWidget(lvl1, 0, 0)
        grid_layout.addWidget(lvl2, 0, 1)
        grid_layout.addWidget(lvl3, 0, 2)
        grid_layout.addWidget(lvl4, 0, 3)
        grid_layout.addWidget(lvl5, 0, 4)
        grid_layout.addWidget(lvl6, 1, 0)
        grid_layout.addWidget(lvl7, 1, 1)
        grid_layout.addWidget(lvl8, 1, 2)
        grid_layout.addWidget(lvl9, 1, 3)
        grid_layout.addWidget(lvl10, 1, 4)


        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

    def showEvent(self, event):
        self.play_instruction_sound()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def play_instruction_sound(self):
        sound_path = os.path.abspath(os.path.join(INSTRUCTION_SOUNDS_DIR, INSTRUCTION_SOUND_FILE))
        if os.path.exists(sound_path):
            self.instruction_player.stop()
            self.instruction_player.setSource(QUrl.fromLocalFile(sound_path))
            self.instruction_player.play()
        else:
            print(f"Instruction sound not found: {sound_path}")

    def stop_instruction_sound(self):
        self.instruction_player.stop()
