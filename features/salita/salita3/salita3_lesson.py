import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import * 
from themes.fonts import BODY_FONT
from components.choices_button import ChoicesButton
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "salita")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "Salita")
INSTRUCTION_SOUND_FILE = "Pangungusap.mp3"


class Salita3(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        #top layout| back buttonnnn
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(60, 50, 0, 20)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("grade1_dash"))

        pagsasanay = QLabel("Aralin 3: Pangungusap")
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

        content_layout = QHBoxLayout()
        content_layout.setSpacing(5)
        main_layout.addLayout(content_layout)

    
        lesson = QVBoxLayout()
        lesson.setSpacing(10)
        content_layout.addLayout(lesson)

        # Title
        title = QLabel("Ano ang Pangungusap?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 700; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        lesson.addWidget(title)

        # Illustration
        image = QLabel()
        image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "pangungusap.png")).scaled(
                160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image.setAlignment(Qt.AlignCenter)
        lesson.addWidget(image)


        # Speaker icon + text row
        text_row = QHBoxLayout()
        text_row.setSpacing(15)
        text_row.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        lesson_text = QLabel(
            "Ito ay grupo ng mga salita na may <b>BUONG DIWA,</b>\n" 
            "binubuo ito ng simuno at panaguri. Ang <b>simuno</b>\n" 
            "(paksa) ay ang bahagi ng pangungusap na\n" 
            "pinag-uusapan. Habang ang <b>panaguri</b> ay ang \n"
            "nagsasabi ng impormasyon sa simuno. Dapat\n" 
            "din na MALAKI ang unang letra at nagtatapos\n"
            "sa tuldok (.)"

        )
        lesson_text.setAlignment(Qt.AlignLeft)
        lesson_text.setWordWrap(True)   
        lesson_text.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 500;
            font-family: {BODY_FONT};
            color: {CHOCO_BROWN};
        """)
        text_row.addWidget(lesson_text)
        lesson.addLayout(text_row)


        #halimbawa
        example = QVBoxLayout()
        content_layout.addLayout(example)

        # Title
        title = QLabel("Paano bumuo ng Pangungusap?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 700; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        example.addWidget(title)

        # Illustration
        image = QLabel()
        image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "simuno.png")).scaled(
                180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image.setAlignment(Qt.AlignCenter)
        example.addWidget(image)


        # Speaker icon + text row
        text_row = QHBoxLayout()
        text_row.setSpacing(15)
        text_row.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        lesson_text = QLabel(
            "Pagsamahin ang simuno at panaguri.\n" 
            "Halimbawa: \n"
            "Ang pusa ay tumatakbo.\n"
            "Simuno: Ang pusa | Panaguri: tumatakbo\n"
            
        )
        lesson_text.setAlignment(Qt.AlignLeft)
        lesson_text.setWordWrap(True)   
        lesson_text.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 500;
            font-family: {BODY_FONT};
            color: {CHOCO_BROWN};
        """)
        text_row.addWidget(lesson_text)
        example.addLayout(text_row)

        # Illustration
        image = QLabel()
        image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "halimbawa.png")).scaled(
                140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image.setAlignment(Qt.AlignCenter)
        example.addWidget(image)


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
        self.next_btn.clicked.connect(lambda: self.router.navigate("salitaq9"))

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
