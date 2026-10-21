import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from themes.colors import * 
from themes.fonts import BODY_FONT


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "kuwento")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "icons")
PRONUNCIATION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "audio", "VO Kuwento")


class Kuwento8(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.word_audio_output = QAudioOutput(self)
        self.word_player = QMediaPlayer(self)
        self.word_player.setAudioOutput(self.word_audio_output)
        self.word_audio_output.setVolume(1.0)

        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        #top layout| back buttonnnn
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(60, 50, 0, 50)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("kuwento"))

        pagsasanay = QLabel("Kuwento 8")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(30)
        main_layout.addLayout(top_layout)

        # Title
        title = QLabel("Mang Dada")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 600; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        # Illustration
        image = QLabel()
        image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "MD.png")).scaled(
                260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image)

        # Speaker icon + text row
        text_row = QHBoxLayout()
        text_row.setSpacing(15)
        text_row.setAlignment(Qt.AlignCenter)

        self.speaker_btn = QPushButton()
        self.speaker_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "audio_icon.png")))
        self.speaker_btn.setIconSize(QSize(24, 24))
        self.speaker_btn.setFlat(True)
        self.speaker_btn.setCursor(Qt.PointingHandCursor)
        self.speaker_btn.clicked.connect(self.play_word_sound)
        text_row.addWidget(self.speaker_btn, alignment=Qt.AlignmentFlag.AlignTop)

        
        story_text = QLabel(
            "Si Mang Dada ay masipag na magsasaka.\n"
            "Tindi ng sikat ng araw hindi alintana sa kanya.\n"
            "Bawat butil ng palay ay itinanim sa matinding pagod at pawis.\n"
            "Ito ay pagkain ng mayaman at mahirap."
        )
        story_text.setAlignment(Qt.AlignLeft)
        story_text.setWordWrap(True)   
        story_text.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 400;
            font-family: {BODY_FONT};
            color: {CHOCO_BROWN};
        """)
        text_row.addWidget(story_text, 1)

        main_layout.addLayout(text_row)
        main_layout.addStretch()

        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(200)
        lower_layout.setContentsMargins(70, 20, 70, 30)
        main_layout.addLayout(lower_layout)
        
        self.next_btn = QPushButton("Sunod")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
                    background-color: {BRIGHT_YELLOW};
                    color: {CHOCO_BROWN};
                    font-size: 22px;
                    font-weight: 700;
                    border-radius: 6px;
                    font-family: {BODY_FONT};
                """)
        self.next_btn.setFixedSize(180, 50)
        lower_layout.addWidget(self.next_btn, alignment = Qt.AlignmentFlag.AlignRight)
        self.next_btn.clicked.connect(lambda: self.router.navigate("quest8"))
        
        main_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def play_word_sound(self):
        """Plays the target word pronunciation sound."""
        sound_path = os.path.join(
            PRONUNCIATION_SOUNDS_DIR, f"MangDada.mp3"
        )
        if not os.path.exists(sound_path):
            sound_path = os.path.join(
                PRONUNCIATION_SOUNDS_DIR, f"MangDada.wav"
            )

        if os.path.exists(sound_path):
            abs_path = os.path.abspath(sound_path)
            self.word_player.setSource(QUrl.fromLocalFile(abs_path))
            self.word_player.play()
