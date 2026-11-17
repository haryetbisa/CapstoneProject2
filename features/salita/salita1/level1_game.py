import os
import random
from PySide6.QtCore import Qt, QSize, QUrl, QTimer
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
SFX_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "sound_tama_mali")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "Salita")
INSTRUCTION_SOUND_FILE = "sorbetes.mp3" 


class Salita1Game(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Track correctly clicked answers
        self.correct_found = set()
        self.total_correct_answers = 2  # "matamis" and "malamig"

        # Dual Audio Player Setup for Feedback (Voice-over + SFX)
        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(1.5)

        self.sfx_audio_output = QAudioOutput(self)
        self.sfx_player = QMediaPlayer(self)
        self.sfx_player.setAudioOutput(self.sfx_audio_output)
        self.sfx_audio_output.setVolume(0.3)

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(15)

        # Top Navigation Bar
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 10, 20, 10)
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

        pagsasanay = QLabel("Pagsasanay 1: Naglalarawan na Salita")
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

        # Question Title
        title = QLabel("Ano ang mga salita na maaaring maglarawan sa sorbetes?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 600; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        # Image and Choices Container
        choices = QHBoxLayout()
        choices.setContentsMargins(0, 10, 0, 0)
        choices.addSpacing(50)
        main_layout.addLayout(choices)

        # Illustration
        image = QLabel()
        image_path = os.path.join(IMAGE_DIR, "icecream.png")
        if os.path.exists(image_path):
            image.setPixmap(
                QPixmap(image_path).scaled(
                    350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        image.setAlignment(Qt.AlignCenter)
        choices.addWidget(image)

        # Choices Column
        quest_row = QVBoxLayout()
        quest_row.setSpacing(20)
        quest_row.setAlignment(Qt.AlignCenter)

        self.opt_1 = ChoicesButton("matamis", color=CORNFLOWER_BLUE)  # Correct
        self.opt_2 = ChoicesButton("maalat", color=MEDIUM_PURPLE)     # Wrong
        self.opt_3 = ChoicesButton("malamig", color=HONEY_YELLOW)     # Correct

        self.opt_1.clicked.connect(lambda: self.handle_choice(True, self.opt_1, "matamis"))
        self.opt_2.clicked.connect(lambda: self.handle_choice(False, self.opt_2, "maalat"))
        self.opt_3.clicked.connect(lambda: self.handle_choice(True, self.opt_3, "malamig"))

        quest_row.addWidget(self.opt_1)
        quest_row.addWidget(self.opt_2)
        quest_row.addWidget(self.opt_3)
        choices.addLayout(quest_row)

        # Feedback Text Label (Placed right above action buttons)
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet(f"font-size: 24px; font-weight: 700; font-family: {BODY_FONT}; color: transparent;")
        main_layout.addWidget(self.feedback_label)

        # Action Buttons Layout (Restart + Next)
        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.setSpacing(20)

        self.restart_btn = QPushButton("Ulitin")
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
        """Resets choice states, clears answers, clears feedback label, and hides action buttons."""
        self.correct_found.clear()
        self.feedback_label.setText("")
        self.feedback_label.setStyleSheet("color: transparent;")
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
        """Resets game state and routes to the next level."""
        self.reset_game()
        self.router.navigate("salitaq2")

    def play_feedback_sound(self, is_correct: bool):
        """Plays randomized voice-over feedback alongside matching sound effect."""
        if is_correct:
            voice_file, sfx_file = random.choice([
                ("tama_1.mp3", "correct.wav"),
                ("tama_2.mp3", "correct.wav")
            ])
        else:
            voice_file, sfx_file = random.choice([
                ("mali_Ac.mp3", "wrong.wav"),
                ("mali_AC2.mp3", "wrong.wav")
            ])

        sfx_path = os.path.abspath(os.path.join(SFX_SOUNDS_DIR, sfx_file))
        if os.path.exists(sfx_path):
            self.sfx_player.stop()
            self.sfx_player.setSource(QUrl.fromLocalFile(sfx_path))
            self.sfx_player.play()

        voice_path = os.path.abspath(os.path.join(FEEDBACK_SOUNDS_DIR, voice_file))
        if os.path.exists(voice_path):
            self.feedback_player.stop()
            self.feedback_player.setSource(QUrl.fromLocalFile(voice_path))
            self.feedback_player.play()

    def handle_choice(self, is_correct: bool, button: QPushButton, choice_key: str):
        """Handles answer checking, dual audio feedback, dynamic text, auto-restart on error, and locking on completion."""
        self.play_feedback_sound(is_correct)

        if is_correct:
            button.setEnabled(False)
            button.setStyleSheet("background-color: #2ECC71; color: white; border-radius: 10px; font-weight: bold;")
            self.correct_found.add(choice_key)

            # Check if all correct answers are found
            if len(self.correct_found) == self.total_correct_answers:
                self.feedback_label.setText("Magaling! Tama lahat ng iyong sagot!")
                self.feedback_label.setStyleSheet(f"font-size: 24px; font-weight: 700; font-family: {BODY_FONT}; color: #27AE60;")
                
                # Lock remaining buttons and show Ulitin + Susunod
                self.opt_1.setEnabled(False)
                self.opt_2.setEnabled(False)
                self.opt_3.setEnabled(False)
                self.restart_btn.show()
                self.next_btn.show()
                
                # Log progress locally and queue for sync under "Salita"
                self.save_activity_progress("Salita", "salita_q1", 1.0)
            else:
                # First correct answer found, encourage student to find the next one
                self.feedback_label.setText("Magaling! Isa na lang ang hanapin mo!")
                self.feedback_label.setStyleSheet(f"font-size: 24px; font-weight: 700; font-family: {BODY_FONT}; color: #27AE60;")
        else:
            button.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 10px; font-weight: bold;")
            
            # Display wrong feedback message
            self.feedback_label.setText("Mali. Subukan muli! ❌")
            self.feedback_label.setStyleSheet(f"font-size: 24px; font-weight: 700; font-family: {BODY_FONT}; color: #C0392B;")
            
            # Lock all buttons immediately so student cannot click anything else while wrong audio plays
            self.opt_1.setEnabled(False)
            self.opt_2.setEnabled(False)
            self.opt_3.setEnabled(False)

            # Automatically restart activity after 1.5 seconds to let the wrong feedback audio play
            QTimer.singleShot(1500, self.reset_game)

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
            print("--> Salita Q1 activity successfully logged!")
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