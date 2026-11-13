from PySide6.QtCore import Qt, QSize, QUrl
<<<<<<< HEAD
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPushButton, QLineEdit
=======
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
>>>>>>> bebf379e53e85ce54b926e5c30cbb9777426539f
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from themes.colors import *
from themes.fonts import BODY_FONT
from components.lesson_card import LessonCard

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "PNK_Lesson")
INSTRUCTION_SOUND_FILE = "Tainga.mp3"
<<<<<<< HEAD
=======

>>>>>>> bebf379e53e85ce54b926e5c30cbb9777426539f

class LessonScreenTaingaa(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

<<<<<<< HEAD

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60,60,60,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )
=======
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(20)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(25)
>>>>>>> bebf379e53e85ce54b926e5c30cbb9777426539f

        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent; border-radius: 6px;")
        back_btn.clicked.connect(lambda: self.router.navigate("katawan"))

        pagsasanay = QLabel("Aralin: Tainga")
        pagsasanay.setStyleSheet(f"""
            font-size: 32px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        main_layout.addLayout(top_layout)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(50)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(content_layout)

        self.content_image = QLabel()
        self.image_path = os.path.join(IMAGE_DIR, "tainga.png")
        self.content_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.content_image)

        card = LessonCard(
            title="Aralin 4 : TAINGA/TENGA",
            body_text="Ang tenga (o tainga) ay ang bahagi ng katawan na ginagamit sa pandinig ng mga tunog at tumutulong din sa pagpapanatili ng balanse ng katawan."
        )
        content_layout.addWidget(card)

<<<<<<< HEAD

        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(200)
        lower_layout.setContentsMargins(70, 20, 70, 30)
        main_layout.addLayout(lower_layout)


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
        lower_layout.addWidget(self.speak_btn, alignment = Qt.AlignmentFlag.AlignRight)
        self.speak_btn.clicked.connect(lambda: self.router.navigate("tengavs"))

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


=======
        main_layout.addStretch()

        self.speak_btn = QPushButton("Sunod ➔")
        self.speak_btn.setCursor(Qt.PointingHandCursor)
        self.speak_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BRIGHT_YELLOW};
                color: {CHOCO_BROWN};
                font-size: 22px;
                font-weight: 800;
                border-radius: 14px;
                padding: 14px 35px;
                font-family: {BODY_FONT};
            }}
            QPushButton:hover {{
                background-color: #F1C40F;
            }}
        """)
        self.speak_btn.clicked.connect(lambda: self.router.navigate("tengavs"))
        
        main_layout.addWidget(self.speak_btn, alignment=Qt.AlignmentFlag.AlignRight)
>>>>>>> bebf379e53e85ce54b926e5c30cbb9777426539f

        self.update_responsive_scaling()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_responsive_scaling()

    def update_responsive_scaling(self):
        screen_width = self.width()
        screen_height = self.height()
        
        scale_factor = min(screen_width, screen_height)
        img_size = int(scale_factor * 0.38)
        img_size = max(250, min(img_size, 550))

        if os.path.exists(self.image_path):
            self.content_image.setPixmap(QPixmap(self.image_path).scaled(
                img_size, img_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

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