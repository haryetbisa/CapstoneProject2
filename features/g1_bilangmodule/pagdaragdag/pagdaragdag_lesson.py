import os
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "bilang_g1")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class LessonMath7(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
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
        back_btn.clicked.connect(lambda: self.router.navigate("bilang_g1"))

        pagsasanay = QLabel("Aralin: Pagdaragdag (Addition)")
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

        # ---- The video display widget ----
        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(960, 510)
        main_layout.addWidget(self.video_widget, alignment=Qt.AlignCenter)

        # ---- Media player + audio output ----
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)   # connects player's video frames to the widget

        video_path = os.path.join(VIDEO_DIR, "addition.mp4")
        self.player.setSource(QUrl.fromLocalFile(video_path))

        # ---- Controls row ----
        controls = QHBoxLayout()
        controls.setAlignment(Qt.AlignCenter)
        controls.setSpacing(20)

        self.play_pause_btn = QPushButton("▶ Play")
        self.play_pause_btn.setFixedSize(140, 50)
        self.play_pause_btn.setCursor(Qt.PointingHandCursor)
        self.play_pause_btn.setStyleSheet("""
            background-color: #FFD24C;
            color: #3A2E1F;
            font-size: 18px;
            font-weight: 800;
            border-radius: 10px;
        """)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        controls.addWidget(self.play_pause_btn)

        main_layout.addLayout(controls)

        # ---- Keep the button label in sync with actual playback state ----
        self.player.playbackStateChanged.connect(self.update_button_label)

    def toggle_play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def update_button_label(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_pause_btn.setText("⏸ Pause")
        else:
            self.play_pause_btn.setText("▶ Play")