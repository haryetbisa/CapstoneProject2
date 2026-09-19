import os

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

from features.voice_recog import OfflineVoiceWorker
from themes.colors import *
from themes.fonts import BODY_FONT

# Path Configurations
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image_content", "pantig")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(
    BASE_DIR, "assets", "sounds", "correct_&_wrong"
)
PRONUNCIATION_SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds", "pantig")


class PantigAraw(QWidget):

    def __init__(self, router):
        super().__init__()
        self.router = router
        self.target_word = "araw"
        self.worker = None

        
        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(1.0)

       
        self.word_audio_output = QAudioOutput(self)
        self.word_player = QMediaPlayer(self)
        self.word_player.setAudioOutput(self.word_audio_output)
        self.word_audio_output.setVolume(1.0)

       
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)

        # Top Navigation Bar
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_bar.setSpacing(20)

        back_btn = QPushButton()
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

        pagsasanay = QLabel("Pagsasanay")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};
        """)

        top_bar.addWidget(back_btn)
        top_bar.addWidget(pagsasanay)
        main_layout.addLayout(top_bar)

        # Main Graphic (aso.png)
        image = QLabel()
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_path = os.path.join(IMAGE_DIR, "araw.png")
        if os.path.exists(image_path):
            image.setPixmap(
                QPixmap(image_path).scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        main_layout.addWidget(image)

        # Word Display Layout
        word_layout = QHBoxLayout()
        word_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word_layout.setSpacing(20)

        self.audio = QPushButton()
        audio_icon_path = os.path.join(ICONS_DIR, "audio_icon.png")
        if os.path.exists(audio_icon_path):
            self.audio.setIcon(QIcon(audio_icon_path))
        self.audio.setIconSize(QSize(40, 40))
        self.audio.setCursor(Qt.PointingHandCursor)
        self.audio.setStyleSheet(
            "border: none; background-color: transparent;"
        )
        self.audio.clicked.connect(self.play_word_sound)
        word_layout.addWidget(self.audio)

        salita = QLabel("A-raw")
        salita.setStyleSheet(f"""
            font-size: 96px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};
        """)
        word_layout.addWidget(salita)
        main_layout.addLayout(word_layout)

        # Microphone Action Button
        self.speak_btn = QPushButton("I-TAP KAPAG MAG-SASALITA")
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

        # Result / Feedback Label
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setStyleSheet(f"""
            font-size: 24px;
            font-family: {BODY_FONT};
            font-weight: bold;
            color: {CHOCO_BROWN};
        """)
        main_layout.addWidget(self.feedback_label)

        main_layout.setSpacing(20)
        main_layout.addStretch(1)

        # Lower Navigation Bar (Next Button)
        lower_layout = QHBoxLayout()
        lower_layout.setContentsMargins(20, 10, 20, 30)

        self.next_btn = QPushButton("Sunod")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BRIGHT_YELLOW};
                color: {CHOCO_BROWN};
                font-size: 22px;
                font-weight: 800;
                border-radius: 6px;
                font-family: {BODY_FONT};
            }}
        """)
        self.next_btn.setFixedSize(240, 60)
        self.next_btn.clicked.connect(
            lambda: self.router.navigate("A_game")
        )

        lower_layout.addStretch()
        lower_layout.addWidget(self.next_btn)
        main_layout.addLayout(lower_layout)

    def play_word_sound(self):
        """Plays the target word pronunciation sound."""
        sound_path = os.path.join(
            PRONUNCIATION_SOUNDS_DIR, f"{self.target_word}.mp3"
        )
        if not os.path.exists(sound_path):
            sound_path = os.path.join(
                PRONUNCIATION_SOUNDS_DIR, f"{self.target_word}.wav"
            )

        if os.path.exists(sound_path):
            abs_path = os.path.abspath(sound_path)
            self.word_player.setSource(QUrl.fromLocalFile(abs_path))
            self.word_player.play()

    def play_feedback_sound(self, filename: str):
        """Plays correct/wrong feedback SFX."""
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            abs_path = os.path.abspath(sound_path)
            self.feedback_player.setSource(QUrl.fromLocalFile(abs_path))
            self.feedback_player.play()

    @Slot()
    def start_listening(self):
        """Starts background voice recognition."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()

        self.speak_btn.setEnabled(False)

        self.feedback_label.setStyleSheet(
            f"font-size: 24px; color: {CHOCO_BROWN}; font-family: {BODY_FONT}; font-weight: bold;"
        )
        self.feedback_label.setText("Nakikinig... Magsalita na!")

        self.worker = OfflineVoiceWorker()
        self.worker.status_changed.connect(self.update_status)
        self.worker.text_recognized.connect(self.evaluate_answer)
        self.worker.finished.connect(self.on_speech_finished)
        self.worker.start()

    @Slot(str)
    def update_status(self, text):
        """Updates live status feedback while listening."""
        if (
            "MAGALING" not in self.feedback_label.text()
            and not self.speak_btn.isEnabled()
        ):
            self.feedback_label.setText(text)

    @Slot(str)
    def evaluate_answer(self, spoken_text):
        """Evaluates recognized text against target word using exact word matching."""
        spoken_clean = spoken_text.lower().replace("-", " ").strip()
        target_clean = self.target_word.lower().strip()

        spoken_words = spoken_clean.split()

        if target_clean in spoken_words:
            self.feedback_label.setText("✅ MAGALING! TAMA!")
            self.feedback_label.setStyleSheet(
                f"font-size: 28px; color: green; font-family: {BODY_FONT}; font-weight: bold;"
            )
            self.play_feedback_sound("correct.wav")
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

    def handle_back(self):
        """Safely stops recording before navigating back."""
        self.stop_worker()
        self.router.navigate("aklat")

    def stop_worker(self):
        """Safely terminates active voice worker threads."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()

    def hideEvent(self, event):
        """Ensures worker thread stops when widget is hidden or navigated away from."""
        self.stop_worker()
        super().hideEvent(event)