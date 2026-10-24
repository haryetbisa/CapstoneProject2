import os
import sys

# Ensure project root is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from components.lesson_card import LessonCard
from themes.colors import *
from themes.fonts import BODY_FONT

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds", "hayop")


class LessonScreenKabayo(QWidget):

    def __init__(self, router):
        super().__init__()
        self.router = router

        # Initialize Audio Player for Animal Sound
        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Top Bar Navigation
        top_layout = QHBoxLayout()
        top_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter
        )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(
            "border: none; background-color: transparent; border-radius: 6px;"
        )
        back_btn.clicked.connect(lambda: self.router.navigate("hayop"))

        pagsasanay = QLabel("Aralin: Kabayo")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(20)
        main_layout.addLayout(top_layout)

        # Main Content Layout (Left Column: Image + Play Btn | Right Column: Card + Sunod Btn)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(70, 0, 70, 0)
        content_layout.setSpacing(120)

        # --- LEFT COLUMN (Image + Centered Play Button) ---
        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_column.setSpacing(30)

        content_image = QLabel()
        content_image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "kabayo.png")).scaled(
                380, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
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

        card = LessonCard(
            title="Aralin 5 : KABAYO",
            body_text=(
                "Ang kabayo ay isang malaking hayop na inaalagaan ng mga tao na"
                " may apat na paa at matitigas na kuko. Kilala sila sa"
                " pagkakaroon ng mahabang buhok sa leeg , mahabang buntot, at"
                " mabilis na pagtakbo."
            ),
        )
        right_column.addWidget(card)

        self.speak_btn = QPushButton("Sunod")
        self.speak_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "mic_icon.png")))
        self.speak_btn.setIconSize(QSize(30, 30))
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
        self.speak_btn.clicked.connect(
            lambda: self.router.navigate("kabayovs")
        )
        right_column.addWidget(
            self.speak_btn, alignment=Qt.AlignmentFlag.AlignRight
        )

        content_layout.addLayout(right_column)
        main_layout.addLayout(content_layout)

    def play_animal_sound(self):
        """Plays the animal sound clip from assets/sounds/hayop/."""
        sound_path = os.path.join(SOUNDS_DIR, "kabayo.mp3")

        if not os.path.exists(sound_path):
            sound_path = os.path.join(SOUNDS_DIR, "kabayo.wav")

        if os.path.exists(sound_path):
            self.player.setSource(QUrl.fromLocalFile(sound_path))
            self.player.play()
        else:
            print(f"Animal sound file missing: {sound_path}")