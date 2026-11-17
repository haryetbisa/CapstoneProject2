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
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "kuwento")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "icons")
SFX_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "sounds", "correct_&_wrong")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "sounds", "sound_tama_mali")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "audio", "KuwentoQuestions")
INSTRUCTION_SOUND_FILE = "Tanong 8.mp3" 


class Kuwento8Question(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

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

        # Header Navigation Bar
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

        pagsasanay = QLabel("Kuwento 8: Mang Dada")
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
        title = QLabel("Ano ang trabaho ni Mang Dada?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        # Image Container
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

        # Multiple Choice Options
        quest_row = QHBoxLayout()
        quest_row.setSpacing(29)
        quest_row.setAlignment(Qt.AlignCenter)

        self.opt_1 = ChoicesButton("guro", color=SKY_BLUE)
        self.opt_2 = ChoicesButton("magsasaka", color=HOT_PINK)
        self.opt_3 = ChoicesButton("doktor", color=LIGHT_GREEN)

        self.opt_1.clicked.connect(lambda: self.handle_choice(False, self.opt_1))
        self.opt_2.clicked.connect(lambda: self.handle_choice(True, self.opt_2))
        self.opt_3.clicked.connect(lambda: self.handle_choice(False, self.opt_3))

        quest_row.addWidget(self.opt_1)
        quest_row.addWidget(self.opt_2)
        quest_row.addWidget(self.opt_3)
        main_layout.addLayout(quest_row)

        # Feedback Text Label
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
        self.feedback_label.setText("")
        self.feedback_label.setStyleSheet("color: transparent;")
        self.restart_btn.hide()
        self.next_btn.hide()
        
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
        self.play_instruction_sound()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("level8")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("level9")

    def play_feedback_sound(self, is_correct: bool):
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

    def handle_choice(self, is_correct: bool, button: QPushButton):
        self.play_feedback_sound(is_correct)

        self.opt_1.setEnabled(False)
        self.opt_2.setEnabled(False)
        self.opt_3.setEnabled(False)

        if is_correct:
            button.setStyleSheet("background-color: #2ECC71; color: white; border-radius: 10px; font-weight: bold;")
            self.feedback_label.setText("Magaling! Tama ang iyong sagot!")
            self.feedback_label.setStyleSheet(f"font-size: 24px; font-weight: 700; font-family: {BODY_FONT}; color: #27AE60;")
            self.restart_btn.show()
            self.next_btn.show()
            self.save_activity_progress("Kuwento", "kuwento_q8", 1.0)
        else:
            button.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 10px; font-weight: bold;")
            self.feedback_label.setText("Mali. Subukan muli!")
            self.feedback_label.setStyleSheet(f"font-size: 24px; font-weight: 700; font-family: {BODY_FONT}; color: #C0392B;")
            self.restart_btn.show()
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
            print("--> Kuwento Q8 activity successfully logged!")
        except Exception as e:
            print(f"--> Error logging activity progress: {e}")

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