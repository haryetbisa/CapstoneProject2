import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import * 
from themes.fonts import BODY_FONT
from components.choices_button import ChoicesButton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "kuwento")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "sounds", "correct_&_wrong")

class Kuwento8Question(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(0.8)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(60, 50, 0, 20)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent; border-radius: 6px;")
        back_btn.clicked.connect(self.handle_back)

        pagsasanay = QLabel("Kuwento 7: Mang Dada")
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

        title = QLabel("Ano ang trabaho ni Mang Dada")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        image = QLabel()
        image_path = os.path.join(IMAGE_DIR, "MD.png")
        if os.path.exists(image_path):
            image.setPixmap(
                QPixmap(image_path).scaled(
                    200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image)

        quest_row = QHBoxLayout()
        quest_row.setSpacing(29)
        quest_row.setAlignment(Qt.AlignCenter)

        self.opt_1 = ChoicesButton("guro", color=SKY_BLUE)
        self.opt_2 = ChoicesButton("magsasaka", color=HOT_PINK)
        self.opt_3 = ChoicesButton("doktor", color=LIGHT_GREEN)

        self.opt_1.clicked.connect(lambda: self.handle_choice(False, self.opt_1))
        self.opt_2.clicked.connect(lambda: self.handle_choice(False, self.opt_2))
        self.opt_3.clicked.connect(lambda: self.handle_choice(True, self.opt_3))

        quest_row.addWidget(self.opt_1)
        quest_row.addWidget(self.opt_2)
        quest_row.addWidget(self.opt_3)
        main_layout.addLayout(quest_row)

        restart_layout = QHBoxLayout()
        restart_layout.setAlignment(Qt.AlignCenter)

        self.restart_btn = QPushButton(" Restart")
        restart_icon_path = os.path.join(ICONS_DIR, "reset_icon.png")
        if os.path.exists(restart_icon_path):
            self.restart_btn.setIcon(QIcon(restart_icon_path))
        self.restart_btn.setCursor(Qt.PointingHandCursor)
        self.restart_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MARIGOLD};
                color: white;
                font-family: {BODY_FONT};
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 24px;
            }}
            QPushButton:hover {{
                background-color: #E08E00;
            }}
        """)
        self.restart_btn.hide()
        self.restart_btn.clicked.connect(self.reset_game)

        restart_layout.addWidget(self.restart_btn)
        main_layout.addLayout(restart_layout)

        main_layout.addStretch()

    def reset_game(self):
        self.restart_btn.hide()
        
        button_configs = [
            (self.opt_1, SKY_BLUE),
            (self.opt_2, HOT_PINK),
            (self.opt_3, LIGHT_GREEN),
        ]
        
        for opt, color in button_configs:
            opt.setEnabled(True)
            if hasattr(opt, "reset"):
                opt.reset()
            else:
                opt.setStyleSheet(f"background-color: {color}; color: white; border-radius: 10px; font-weight: bold;")

    def showEvent(self, event):
        self.reset_game()
        super().showEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("level1")

    def play_feedback_sound(self, is_correct: bool):
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

    def handle_choice(self, is_correct: bool, button: QPushButton):
        self.play_feedback_sound(is_correct)

        if is_correct:
            button.setEnabled(False)
            button.setStyleSheet("background-color: #2ECC71; color: white; border-radius: 10px; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 10px; font-weight: bold;")

        self.restart_btn.show()