from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPushButton, QLineEdit
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from components.cardsbutton import CardsButton
from themes.colors import *
from assets.icon import icon_label
from themes.fonts import  BODY_FONT
from components.lesson_card import LessonCard

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..","..", "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "hayop")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "HayopLesson")
INSTRUCTION_SOUND_FILE = "Kambing.mp3"


class LessonScreenKambing(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        # Initialize Audio Player
        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60,60,60,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("hayop"))

   
        pagsasanay = QLabel("Aralin: Kambing")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        
        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(50)
        main_layout.addLayout(top_layout)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(70, 20, 70, 30)
        content_layout.setSpacing(280)
        main_layout.addLayout(content_layout)

        # --- LEFT COLUMN (Image + Centered Play Button Below It) ---
        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_column.setSpacing(30)

        #yung image
        content_image = QLabel()
        content_image.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "kambing.png")).scaled(
                380, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        content_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_column.addWidget(content_image)

        self.audio_btn = QPushButton(self)
        self.audio_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "play.png")))
        self.audio_btn.setIconSize(QSize(80, 80))
        self.audio_btn.setFlat(True)
        self.audio_btn.setCursor(Qt.PointingHandCursor)
        self.audio_btn.setStyleSheet(
            "border: none; background-color: transparent;"
        )
        self.audio_btn.clicked.connect(self.play_animal_sound)
        left_column.addWidget(
            self.audio_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        content_layout.addLayout(left_column)

        # --- RIGHT COLUMN (Lesson Card + Sunod Button) ---
        right_column = QVBoxLayout()
        right_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_column.setSpacing(30)

        #lesson explanation
        card = LessonCard(
        title="Aralin 7 : KAMBING",
        body_text="Ang kambing ay isang uri ng alagang hayop sa bukid na may apat na paa at karaniwang may dalawang sungay. Ang kinakain lamang nila ay damo, dahon, at sanga ng kahoy.")
        right_column.addWidget(card)


        self.speak_btn = QPushButton("Sunod")
        self.speak_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "mic_icon.png")))
        self.speak_btn.setIconSize(QSize(30, 30))
        self.speak_btn.setFixedHeight(40)
        self.speak_btn.setCursor(Qt.PointingHandCursor)
        self.speak_btn.setStyleSheet(f"""
            background-color: {BRIGHT_YELLOW};
            color: {CHOCO_BROWN};
            font-size: 22px;
            font-weight: 800;
            border-radius: 6px;
            font-family: {BODY_FONT};
        """)
        self.speak_btn.setFixedSize(240, 70)
        right_column.addWidget(self.speak_btn, alignment = Qt.AlignmentFlag.AlignRight)
        self.speak_btn.clicked.connect(lambda: self.router.navigate("kambingvs"))

        content_layout.addLayout(right_column)


    def play_animal_sound(self):
        """Plays animal sound if available."""
        sound_path = os.path.join(SOUNDS_DIR, "kambing.mp3")

        if not os.path.exists(sound_path):
            sound_path = os.path.join(SOUNDS_DIR, "kambing.wav")

        if os.path.exists(sound_path):
            self.player.setSource(QUrl.fromLocalFile(sound_path))
            self.player.play()
        else:
            print(f"Animal sound file missing: {sound_path}")

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