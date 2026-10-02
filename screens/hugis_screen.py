from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from themes.fonts import HEADING_FONT, BODY_FONT
from components.cardspng import CardsPicButton
from themes.colors import *

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds", "bgm")
INSTRUCTION_SOUND_FILE = "Up-on-a-Housetop.mp3"


class HugisScreen(QWidget):
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
        back_btn.clicked.connect(lambda: self.router.navigate("kindergarten"))

   
        pagsasanay = QLabel("Pagsasanay")
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


        bilog_card = CardsPicButton("bilog.png", color = CORAL_RED)
        bilog_card.clicked.connect(lambda: self.router.navigate("bilog"))

        tatsu_card = CardsPicButton("tatsulok.png", color = MARIGOLD)
        tatsu_card.clicked.connect(lambda: self.router.navigate("tatsu"))

        parisukat_card = CardsPicButton("parisukat.png", color = ELECTRIC_VIOLET)
        parisukat_card.clicked.connect(lambda: self.router.navigate("parisukat"))

        puso_card = CardsPicButton("puso.png", color = HOT_PINK)
        puso_card.clicked.connect(lambda: self.router.navigate("puso"))

        oblong_card = CardsPicButton("oblong.png", color = SKY_BLUE)
        oblong_card.clicked.connect(lambda: self.router.navigate("oblong"))

        parihaba_card = CardsPicButton("parihaba.png", color = LIGHT_GREEN)
        parihaba_card.clicked.connect(lambda: self.router.navigate("parihaba"))

        bituin_card = CardsPicButton("bituin.png", color = COBALT_BLUE)
        bituin_card.clicked.connect(lambda: self.router.navigate("star"))

        rombus_card = CardsPicButton("brilyante.png", color = TERRACOTTA )
        rombus_card.clicked.connect(lambda: self.router.navigate("diamond"))

        
        grid_layout.addWidget(bilog_card, 0, 0)
        grid_layout.addWidget(tatsu_card, 0, 1)
        grid_layout.addWidget(parisukat_card, 0, 2)
        grid_layout.addWidget(puso_card, 0, 3)
        grid_layout.addWidget(oblong_card, 0, 4)
        grid_layout.addWidget(parihaba_card, 1, 0)
        grid_layout.addWidget(bituin_card, 1, 1)
        grid_layout.addWidget(rombus_card, 1, 2)


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
