

import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import * 
from themes.fonts import BODY_FONT
from components.choices_button import ChoicesButton
from Database.queries import log_activity
from session import AppSession

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "salita")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "Salita")
INSTRUCTION_SOUND_FILE = "parke.mp3" 


class Salita4Game(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Track correctly clicked answers
        self.correct_found = set()
        self.total_correct_answers = 2  # "malawak" and "maingay"

        # Audio Player Setup for SFX
        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(0.8)

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        # Top layout | Back Button
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

        pagsasanay = QLabel("Pagsasanay 4: Naglalarawan na Salita")
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
        title = QLabel("Anong mga salita ang maaaring maglarawan sa parke?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 600; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        # Image and Choices Container
        choices = QHBoxLayout()
        choices.setContentsMargins(0, 50, 0, 0)
        choices.addSpacing(50)
        main_layout.addLayout(choices)

        # Illustration
        image = QLabel()
        image_path = os.path.join(IMAGE_DIR, "park.png")
        if os.path.exists(image_path):
            image.setPixmap(
                QPixmap(image_path).scaled(
                    380, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        image.setAlignment(Qt.AlignCenter)
        choices.addWidget(image)

        # Choices Column
        quest_row = QVBoxLayout()
        quest_row.setSpacing(20)
        quest_row.setAlignment(Qt.AlignCenter)

        self.opt_1 = ChoicesButton("malawak", color=CORNFLOWER_BLUE)   # Correct
        self.opt_2 = ChoicesButton("maingay", color=MEDIUM_PURPLE)    # Correct
        self.opt_3 = ChoicesButton("matamis", color=HONEY_YELLOW)      # Wrong

        self.opt_1.clicked.connect(lambda: self.handle_choice(True, self.opt_1, "malawak"))
        self.opt_2.clicked.connect(lambda: self.handle_choice(True, self.opt_2, "maingay"))
        self.opt_3.clicked.connect(lambda: self.handle_choice(False, self.opt_3, "matamis"))

        quest_row.addWidget(self.opt_1)
        quest_row.addWidget(self.opt_2)
        quest_row.addWidget(self.opt_3)
        choices.addLayout(quest_row)

        # Action Buttons Layout (Restart + Next)
        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.setSpacing(20)

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

        self.next_btn = QPushButton("Susunod ➔")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2E7D32;
                color: white;
                font-family: {BODY_FONT};
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 24px;
            }}
            QPushButton:hover {{
                background-color: #1B5E20;
            }}
        """)
        self.next_btn.hide()
        self.next_btn.clicked.connect(self.handle_next)

        action_layout.addWidget(self.restart_btn)
        action_layout.addWidget(self.next_btn)
        main_layout.addLayout(action_layout)

        main_layout.addStretch()

    def reset_game(self):
        """Resets choice states, clears selected answers, and hides action buttons."""
        self.correct_found.clear()
        self.restart_btn.hide()
        self.next_btn.hide()

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

    def handle_back(self):
        """Resets game state and routes back."""
        self.reset_game()
        self.router.navigate("salita")

    def handle_next(self):
        """Resets game state and routes forward to Pagsasanay 5."""
        self.reset_game()
        self.router.navigate("salita2")

    def play_feedback_sound(self, is_correct: bool):
        """Plays correct or wrong SFX."""
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.stop()
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

    def handle_choice(self, is_correct: bool, button: QPushButton, choice_key: str):
        """Handles choice selection, plays sound, and toggles navigation buttons."""
        self.play_feedback_sound(is_correct)

        if is_correct:
            button.setEnabled(False)
            button.setStyleSheet("background-color: #2ECC71; color: white; border-radius: 10px; font-weight: bold;")
            self.correct_found.add(choice_key)

            if len(self.correct_found) == self.total_correct_answers:
                self.restart_btn.show()
                self.next_btn.show()
                # Log progress locally and queue for sync under "Salita"
                self.save_activity_progress("Salita", "salita_q4", 1.0)
        else:
            button.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 10px; font-weight: bold;")
            self.restart_btn.show()

    def save_activity_progress(self, module_name, target_word, score):
        try:
            student_id = AppSession.get_active_student_id()
            if not student_id:
                print("--> No active student selected for activity logging.")
                return
            log_activity(
                student_id=student_id,
                module_name=module_name,
                score=score,
                target_word=target_word,
                attempts=1
            )
            print("--> Salita Q4 activity successfully logged!")
        except Exception as e:
            print(f"--> Error logging activity progress: {e}")

    def showEvent(self, event):
        self.reset_game()
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