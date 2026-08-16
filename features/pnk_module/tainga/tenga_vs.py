import os

from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from themes.colors import *
from themes.fonts import BODY_FONT

from features.voice_recog import OfflineVoiceWorker


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")


class TengaVS(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.target_words = ["tainga", "tenga"]
        self.worker = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)

        # Top Navigation Bar
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        back_btn = QPushButton(self)
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent; border-radius: 6px;")
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

        # Main Graphic Image Label
        image = QLabel(self)
        image_path = os.path.join(IMAGE_DIR, "tainga.png")
        if os.path.exists(image_path):
            image.setPixmap(QPixmap(image_path).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(image)

        # Word Display Layout
        word = QHBoxLayout()
        word.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word.setSpacing(20)

        self.audio = QPushButton(self)
        audio_icon_path = os.path.join(ICONS_DIR, "audio_icon.png")
        if os.path.exists(audio_icon_path):
            self.audio.setIcon(QIcon(audio_icon_path))
        self.audio.setIconSize(QSize(40, 40))
        self.audio.setCursor(Qt.PointingHandCursor)
        word.addWidget(self.audio)

        salita = QLabel("Te-nga", self)
        salita.setStyleSheet(f"""
            font-size: 96px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};             
        """)
        word.addWidget(salita)
        main_layout.addLayout(word)

        # Microphone Action Button
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
        main_layout.addWidget(self.speak_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Result / Feedback Label
        self.feedback_label = QLabel("", self)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setStyleSheet(f"""
            font-size: 24px;
            font-family: {BODY_FONT};
            font-weight: bold;
            color: {CHOCO_BROWN};
        """)
        main_layout.addWidget(self.feedback_label)

        main_layout.setSpacing(20)
        main_layout.addStretch(3)

    @Slot()
    def start_listening(self):
        """Starts background voice recognition."""
        self.stop_worker()

        self.speak_btn.setEnabled(False)
        self.feedback_label.setStyleSheet(f"font-size: 24px; color: {CHOCO_BROWN}; font-family: {BODY_FONT}; font-weight: bold;")
        self.feedback_label.setText("Nakikinig... Magsalita na!")

        self.worker = OfflineVoiceWorker()
        self.worker.status_changed.connect(self.update_status)
        self.worker.text_recognized.connect(self.evaluate_answer)
        self.worker.finished.connect(self.on_speech_finished)
        self.worker.start()

    @Slot(str)
    def update_status(self, text):
        """Updates live status feedback while listening."""
        if "MAGALING" not in self.feedback_label.text() and not self.speak_btn.isEnabled():
            self.feedback_label.setText(text)

    @Slot(str)
    def evaluate_answer(self, spoken_text):
        """Evaluates recognized text using target word matches."""
        spoken_clean = spoken_text.lower().replace("-", "").replace(" ", "").strip()
        is_correct = any(target in spoken_clean for target in self.target_words)

        if is_correct:
            self.feedback_label.setText("✅ MAGALING! TAMA!")
            self.feedback_label.setStyleSheet(f"font-size: 28px; color: #2E7D32; font-family: {BODY_FONT}; font-weight: bold;")
        else:
            self.feedback_label.setText(f"❌ SUBUKAN ULIT (Narinig: '{spoken_text}')")
            self.feedback_label.setStyleSheet(f"font-size: 24px; color: #D32F2F; font-family: {BODY_FONT}; font-weight: bold;")

    @Slot()
    def on_speech_finished(self):
        self.speak_btn.setEnabled(True)

    def stop_worker(self):
        """Cleanly stops the thread if running."""
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
        """Safely stops recording before navigating back."""
        self.stop_worker()
        self.router.navigate("tenga")

    def closeEvent(self, event):
        """Ensures thread cleanup when widget is closed."""
        self.stop_worker()
        event.accept()