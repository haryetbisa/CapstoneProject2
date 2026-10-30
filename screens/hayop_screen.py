import os
from PySide6.QtCore import Qt,QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from themes.fonts import BODY_FONT
from session import AppSession


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds", "bgm")
INSTRUCTION_SOUND_FILE = "Up-on-a-Housetop.mp3"

from components.cardspng import CardsPicButton
from themes.colors import *


class HayopScreen(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_player.setLoops(QMediaPlayer.Infinite)  # Loop BGM automatically

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer_layout.addWidget(scroll)

        
        content = QWidget()
        main_layout = QVBoxLayout(content)
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


        aso_card = CardsPicButton ("aso.png", color = CORAL_RED)
        aso_card.clicked.connect(lambda: self.router.navigate("aso_lesson"))

        baboy_card = CardsPicButton ("baboy.png", color = MARIGOLD)
        baboy_card.clicked.connect(lambda: self.router.navigate("baboy_lesson"))
         
        bibe_card = CardsPicButton ("bibe.png", color = ELECTRIC_VIOLET)
        bibe_card.clicked.connect(lambda: self.router.navigate("bibe_lesson"))

        isda_card = CardsPicButton ("isda.png", color = HOT_PINK)
        isda_card.clicked.connect(lambda: self.router.navigate("isda_lesson"))

        kabayo_card = CardsPicButton ("kabayo.png", color = SKY_BLUE)
        kabayo_card.clicked.connect(lambda: self.router.navigate("kabayo_lesson"))

        kalabaw_card = CardsPicButton ("kalabaw.png", color = LIGHT_GREEN)
        kalabaw_card.clicked.connect(lambda: self.router.navigate("kalabaw_lesson"))

        kambing_card = CardsPicButton ("kambing.png", color = COBALT_BLUE)
        kambing_card.clicked.connect(lambda: self.router.navigate("kambing_lesson"))

        kuneho_card = CardsPicButton ("kuneho.png", color = TERRACOTTA) 
        kuneho_card.clicked.connect(lambda: self.router.navigate("kuneho_lesson"))

        manok_card = CardsPicButton ("manok.png", color = BURNT_ORANGE)
        manok_card.clicked.connect(lambda: self.router.navigate("manok_lesson"))

        pagong_card = CardsPicButton ("pagong.png", color = MAGENTA)
        pagong_card.clicked.connect(lambda: self.router.navigate("pagong_lesson"))


        palaka_card = CardsPicButton ("palaka.png", color = CORAL_RED)
        palaka_card.clicked.connect(lambda: self.router.navigate("palaka_lesson"))
         
        pusa_card = CardsPicButton ("pusa.png", color = MARIGOLD) 
        pusa_card.clicked.connect(lambda: self.router.navigate("pusa_lesson"))

        unggoy_card = CardsPicButton ("unggoy.png", color = ELECTRIC_VIOLET) 
        unggoy_card.clicked.connect(lambda: self.router.navigate("unggoy_lesson"))
      
        

        grid_layout.addWidget(aso_card, 0, 0)
        grid_layout.addWidget(baboy_card, 0, 1)
        grid_layout.addWidget(bibe_card, 0, 2)
        grid_layout.addWidget(isda_card, 0, 3)
        grid_layout.addWidget(kabayo_card, 0, 4)

        grid_layout.addWidget(kalabaw_card, 1, 0)
        grid_layout.addWidget(kambing_card, 1, 1)
        grid_layout.addWidget(kuneho_card, 1, 2)
        grid_layout.addWidget(manok_card, 1, 3)
        grid_layout.addWidget(pagong_card, 1, 4)

        grid_layout.addWidget(palaka_card, 2, 0)
        grid_layout.addWidget(pusa_card, 2, 1)
        grid_layout.addWidget(unggoy_card, 2, 2)
    

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)


    def showEvent(self, event):
        self.play_instruction_sound()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def play_instruction_sound(self):
        sound_path = os.path.abspath(os.path.join(INSTRUCTION_SOUNDS_DIR, INSTRUCTION_SOUND_FILE))
        if os.path.exists(sound_path):
            current_vol = AppSession.get_music_volume() if hasattr(AppSession, 'get_music_volume') else 0.7
            self.instruction_audio_output.setVolume(current_vol)

            self.instruction_player.stop()
            self.instruction_player.setSource(QUrl.fromLocalFile(sound_path))
            self.instruction_player.play()
        else:
            print(f"Instruction sound not found: {sound_path}")

    def stop_instruction_sound(self):
        if self.instruction_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.instruction_player.stop()