import os

from features.voice_recog import OfflineVoiceWorker
from PySide6.QtCore import QSize, Qt, QUrl, Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from themes.colors import *
from themes.fonts import BODY_FONT
from session import AppSession
from Database.queries import log_activity

# Resolve project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(
    BASE_DIR, "assets", "sounds", "correct_&_wrong"
)
PRONUNCIATION_SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "audio", "VS PNK")


class MataVS(QWidget):

    def __init__(self, router):
        super().__init__()
        self.router = router
        self.target_word = "mata"
        self.worker = None
        self.score_logged = False  # Prevent duplicate logging per run

        # Audio Output & Player Setup
        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        self.word_audio_output = QAudioOutput(self)
        self.word_player = QMediaPlayer(self)
        self.word_player.setAudioOutput(self.word_audio_output)
        self.word_audio_output.setVolume(1.0)


        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)

        # Top Bar
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        back_btn = QPushButton(self)
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(
            "border: none; background-color: transparent; border-radius: 6px;"
        )
        back_btn.clicked.connect(self.handle_back)

        pagsasanay = QLabel("Pagsasanay", self)
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};             
        """)

        top_bar.addWidget(back_btn)
        top_bar.addWidget(pagsasanay)
        top_bar.setSpacing(20)
        main_layout.addLayout(top_bar)

        # Graphic Image Label
        self.image = QLabel(self)
        image_path = os.path.join(IMAGE_DIR, "mata.png")
        if os.path.exists(image_path):
            self.image.setPixmap(
                QPixmap(image_path).scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image)

        # Word Display & Audio Playback Button
        word = QHBoxLayout()
        word.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word.setSpacing(20)

        self.audio_btn = QPushButton(self)
        audio_icon_path = os.path.join(ICONS_DIR, "audio_icon.png")
        if os.path.exists(audio_icon_path):
            self.audio_btn.setIcon(QIcon(audio_icon_path))
        self.audio_btn.setIconSize(QSize(40, 40))
        self.audio_btn.setCursor(Qt.PointingHandCursor)
        self.audio_btn.setStyleSheet("border: none; background: transparent;")
        self.audio_btn.clicked.connect(self.play_word_audio)
        word.addWidget(self.audio_btn)

        salita = QLabel("Ma-ta", self)
        salita.setStyleSheet(f"""
            font-size: 96px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};             
        """)
        word.addWidget(salita)
        main_layout.addLayout(word)

        # Microphone Button
        self.speak_btn = QPushButton("I-TAP KAPAG MAG-SASALITA", self)
        mic_icon_path = os.path.join(ICONS_DIR, "mic_icon.png")
        if os.path.exists(mic_icon_path):
            self.speak_btn.setIcon(QIcon(mic_icon_path))
        self.speak_btn.setIconSize(QSize(30, 30))
        self.speak_btn.setCursor(Qt.PointingHandCursor)
        self.speak_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BRIGHT_YELLOW};
                color: {CHOCO_BROWN};
                font-size: 20px;
                font-weight: 500;
                border-radius: 6px;
                font-family: {BODY_FONT};
            }}
            QPushButton:disabled {{
                background-color: #D3D3D3;
                color: #888888;
            }}
        """)
        self.speak_btn.setFixedSize(554, 70)
        self.speak_btn.clicked.connect(self.start_listening)
        main_layout.addWidget(
            self.speak_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Feedback Label
        self.feedback_label = QLabel("", self)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setStyleSheet(f"""
            font-size: 24px;
            font-family: {BODY_FONT};
            font-weight: bold;
            color: {CHOCO_BROWN};
        """)
        main_layout.addWidget(self.feedback_label)

        # Susunod Action Button
        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)

        self.next_btn = QPushButton("Susunod ➔", self)
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
        action_layout.addWidget(self.next_btn)
        main_layout.addLayout(action_layout)

        main_layout.setSpacing(20)
        main_layout.addStretch(3)

    def play_word_audio(self):
        sound_path = os.path.join(PRONUNCIATION_SOUNDS_DIR, "Mata.mp3")
        if os.path.exists(sound_path):
            self.player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.player.play()

    def play_feedback_sound(self, filename: str):
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            abs_path = os.path.abspath(sound_path)
            self.player.setSource(QUrl.fromLocalFile(abs_path))
            self.player.play()

    @Slot()
    def start_listening(self):
        self.stop_worker()

        self.speak_btn.setEnabled(False)

        self.feedback_label.setStyleSheet(
            f"font-size: 24px; color: {CHOCO_BROWN}; font-family: {BODY_FONT};"
            " font-weight: bold;"
        )
        self.feedback_label.setText("Nakikinig... Magsalita na!")

        self.worker = OfflineVoiceWorker()
        self.worker.status_changed.connect(self.update_status)
        self.worker.text_recognized.connect(self.evaluate_answer)
        self.worker.finished.connect(self.on_speech_finished)
        self.worker.start()

    @Slot(str)
    def update_status(self, text):
        if (
            "MAGALING" not in self.feedback_label.text()
            and "SUBUKAN" not in self.feedback_label.text()
            and not self.speak_btn.isEnabled()
        ):
            self.feedback_label.setText(text)

    @Slot(str)
    def evaluate_answer(self, spoken_text):
        spoken_clean = spoken_text.lower().replace("-", "").strip()
        target_clean = self.target_word.lower().strip()

        accepted_variants = [
            target_clean,
            "ma ta",
            "ma-ta",
            "mata",
        ]

        is_correct = any(
            variant in spoken_clean for variant in accepted_variants
        )

        if not is_correct:
            has_prefix = any(p in spoken_clean for p in ["ma", "mat"])
            has_suffix = any(s in spoken_clean for s in ["ta", "tha"])
            is_correct = has_prefix and has_suffix

        if is_correct:
            self.feedback_label.setText("✅ MAGALING! TAMA!")
            self.feedback_label.setStyleSheet(
                f"font-size: 28px; color: green; font-family: {BODY_FONT}; font-weight: bold;"
            )
            self.play_feedback_sound("correct.wav")
            self.next_btn.show()

            # --- AUTOMATIC SCORE LOGGING ---
            if not self.score_logged:
                student_id = AppSession.get_active_student_id()
                if student_id:
                    log_activity(
                        student_id=student_id,
                        module_name="Parte ng Katawan",
                        target_word="Mata",
                        score=100.0
                    )
                    print("--> Mata pronunciation score successfully logged!")
                    self.score_logged = True
        else:
            self.feedback_label.setText(
                f"❌ SUBUKAN ULIT (Narinig: '{spoken_text}')"
            )
            self.feedback_label.setStyleSheet(
                f"font-size: 24px; color: red; font-family: {BODY_FONT}; font-weight: bold;"
            )
            self.play_feedback_sound("wrong.wav")

    @Slot()
    def on_speech_finished(self):
        self.speak_btn.setEnabled(True)

    def stop_worker(self):
        if self.worker and self.worker.isRunning():
            try:
                self.worker.status_changed.disconnect()
                self.worker.text_recognized.disconnect()
                self.worker.finished.disconnect()
            except RuntimeError:
                pass
            self.worker.terminate()
            self.worker = None

    def handle_back(self):
        self.stop_worker()
        self.score_logged = False
        self.router.navigate("mata")

    def handle_next(self):
        self.stop_worker()
        self.score_logged = False
        self.router.navigate("labi")

    def closeEvent(self, event):
        self.stop_worker()
        event.accept()