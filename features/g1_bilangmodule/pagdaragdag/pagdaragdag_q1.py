import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import *
from themes.fonts import BODY_FONT
from components.choices_button import ChoicesButton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "bilang_g1")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong")

class BilangLvl9(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Track correctly clicked answers
        self.correct_found = set()
        self.total_correct_answers = 2  # "matamis" and "malamig"

        # Audio Player Setup for SFX
        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(0.8)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        # Top Navigation Bar
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 10)
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

        pagsasanay = QLabel("Pagsasanay 9: Pagdaragdag")
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

        #Horizontal container for image and word problem
        graphics = QHBoxLayout()
        graphics.setAlignment(Qt.AlignCenter)
        graphics.setSpacing(80)
        main_layout.addLayout(graphics)

        #Oliva Container
        sentence1 = QVBoxLayout()
        sentence1.setSpacing(10)
        graphics.addLayout(sentence1)

        oliva = QLabel()
        image_path = os.path.join(IMAGE_DIR, "oliva.png")
        if os.path.exists(image_path):
            oliva.setPixmap(
                QPixmap(image_path).scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        oliva.setAlignment(Qt.AlignCenter)
        sentence1.addWidget(oliva)

        words = QLabel("Si Oliva ay may anim na lobo")
        words.setAlignment(Qt.AlignCenter)
        words.setStyleSheet(f"font-size: 32px; font-weight: 600; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        sentence1.addWidget(words)

        # Oca container
        sentence2 = QVBoxLayout()
        sentence2.setSpacing(10)
        graphics.addLayout(sentence2)

        oca = QLabel()
        image_path = os.path.join(IMAGE_DIR, "oca.png")
        if os.path.exists(image_path):
            oca.setPixmap(
                QPixmap(image_path).scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        oca.setAlignment(Qt.AlignCenter)
        sentence2.addWidget(oca)

        words = QLabel("Si Oca naman ay may tatlong lobo")
        words.setAlignment(Qt.AlignCenter)
        words.setStyleSheet(f"font-size: 32px; font-weight: 600; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        sentence2.addWidget(words)

        # Number and Sign
        number_add = QHBoxLayout()
        number_add.setAlignment(Qt.AlignCenter)
        number_add.setSpacing(200)
        main_layout.addLayout(number_add)

        six = QLabel("6")
        six.setAlignment(Qt.AlignCenter)
        six.setStyleSheet(f"font-size: 50px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        number_add.addWidget(six)

        plus = QLabel("+")
        plus.setAlignment(Qt.AlignCenter)
        plus.setStyleSheet(f"font-size: 50px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        number_add.addWidget(plus)

        three = QLabel("3")
        three.setAlignment(Qt.AlignCenter)
        three.setStyleSheet(f"font-size: 50px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        number_add.addWidget(three)

        equals = QLabel("=")
        equals.setAlignment(Qt.AlignCenter)
        equals.setStyleSheet(f"font-size: 50px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        number_add.addWidget(equals)


        qmark = QLabel("?")
        qmark.setAlignment(Qt.AlignCenter)
        qmark.setStyleSheet(f"font-size: 50px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        number_add.addWidget(qmark)
        
    
        
        # Choices Layout
        quest_row = QHBoxLayout()
        quest_row.setSpacing(20)
        quest_row.setAlignment(Qt.AlignCenter)

        self.opt_1 = ChoicesButton("8", color=CORNFLOWER_BLUE)  # Correct
        self.opt_2 = ChoicesButton("9", color=MEDIUM_PURPLE)     # Wrong
        self.opt_3 = ChoicesButton("7", color=HONEY_YELLOW)     # Correct

        self.opt_1.clicked.connect(lambda: self.handle_choice(True, self.opt_1, "matamis"))
        self.opt_2.clicked.connect(lambda: self.handle_choice(False, self.opt_2, "maalat"))
        self.opt_3.clicked.connect(lambda: self.handle_choice(True, self.opt_3, "malamig"))

        quest_row.addWidget(self.opt_1)
        quest_row.addWidget(self.opt_2)
        quest_row.addWidget(self.opt_3)
        main_layout.addLayout(quest_row)

        # Centered Restart Button Layout (Below Choices)
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
        self.restart_btn.hide()  # Hidden by default
        self.restart_btn.clicked.connect(self.reset_game)

        restart_layout.addWidget(self.restart_btn)
        main_layout.addLayout(restart_layout)

        main_layout.addStretch()

    def reset_game(self):
        """Resets choice states, clears answers, and hides the restart button."""
        self.correct_found.clear()
        self.restart_btn.hide()
        
        button_configs = [
            (self.opt_1, CORNFLOWER_BLUE),
            (self.opt_2, MEDIUM_PURPLE),
            (self.opt_3, HONEY_YELLOW),
        ]
        
        for opt, color in button_configs:
            opt.setEnabled(True)
            if hasattr(opt, "reset"):
                opt.reset()
            else:
                opt.setStyleSheet(f"background-color: {color}; color: white; border-radius: 10px; font-weight: bold;")

    def showEvent(self, event):
        """Resets state whenever screen becomes visible."""
        self.reset_game()
        super().showEvent(event)

    def handle_back(self):
        """Resets game state and routes back."""
        self.reset_game()
        self.router.navigate("bilang_g1")

    def play_feedback_sound(self, is_correct: bool):
        """Plays correct or wrong SFX."""
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

    def handle_choice(self, is_correct: bool, button: QPushButton, choice_key: str):
        """Handles answer checking, plays SFX, and reveals restart button on complete or wrong choice."""
        self.play_feedback_sound(is_correct)

        if is_correct:
            button.setEnabled(False)
            button.setStyleSheet("background-color: #2ECC71; color: white; border-radius: 10px; font-weight: bold;")
            self.correct_found.add(choice_key)

            # Reveal restart button when all correct choices are found
            if len(self.correct_found) == self.total_correct_answers:
                self.restart_btn.show()
        else:
            button.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 10px; font-weight: bold;")
            # Reveal restart button when a wrong choice is picked
            self.restart_btn.show()