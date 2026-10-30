# screens/home_screen.py
import os

from assets.icon import icon_label
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT
from Database.connection import get_db_connection
from session import AppSession

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
SOUNDS_DIR = os.path.join(BASE_DIR, "..", "assets", "sounds", "bgm")

class HomeScreen(QWidget):
    def __init__(self, router, teacher_data=None):
        super().__init__()
        self.router = router
        self.teacher_data = teacher_data or self.get_latest_teacher()

        # Background Music Setup
        self.audio_output = QAudioOutput(self)
        self.media_player = QMediaPlayer(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setLoops(QMediaPlayer.Infinite)  # Loop BGM automatically

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)

        container = QWidget()
        container.setStyleSheet("""
            background-color: #FFD24C; 
            border-radius: 14px;       
        """)
        
        inner_layout = QHBoxLayout(container)
        inner_layout.setContentsMargins(20, 15, 20, 15)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        # Dynamic teacher name greeting
        teacher_name = self.get_current_teacher_name()
        self.hello_text = QLabel(f"Hello, {teacher_name}!")
        self.hello_text.setStyleSheet(f"""
            font-size: 26px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: #3A2E1F;
        """)

        school_name = self.teacher_data.get("school_name", "Paharang Elementary School") if self.teacher_data else "Paharang Elementary School"
        self.welcome_text = QLabel(f"Welcome to BasaMatika - {school_name}")
        self.welcome_text.setStyleSheet(f"""
            font-size: 12px;
            font-family: {BODY_FONT};
            font-weight: 500;
            color: #6B5A3A;
        """)

        text_layout.addWidget(self.hello_text)
        text_layout.addWidget(self.welcome_text)
        inner_layout.addLayout(text_layout)
        inner_layout.addStretch()

        self.g_icon = QPushButton()
        audio_icon_path = os.path.join(ASSETS_DIR, "giraffe.png")
        if os.path.exists(audio_icon_path):
            self.g_icon.setIcon(QIcon(audio_icon_path))
        self.g_icon.setIconSize(QSize(40, 40))
        self.g_icon.setCursor(Qt.PointingHandCursor)
        self.g_icon.setStyleSheet(
            "border: none; background-color: transparent;"
        )
        self.g_icon.clicked.connect(lambda: self.router.navigate("settings"))
        inner_layout.addWidget(self.g_icon)

        main_layout.addWidget(container)

        # 2nd red container
        redcontainer = QWidget()
        redcontainer.setStyleSheet("""
            background-color: #F3554A;
            border-radius: 14px;       
        """)
        
        r_container = QVBoxLayout(redcontainer)
        r_container.setContentsMargins(20, 20, 20, 20)
        
        quote_text = QLabel("BAWAT BATA BUMABASA")
        quote_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_text.setStyleSheet(f"""
            font-size: 60px;
            font-family: {HEADING_FONT};                
            font-weight: 800;
            color: {WHITE};
        """)

        r_container.addWidget(quote_text)
        main_layout.addWidget(redcontainer)
        main_layout.addStretch()

        lower_part = QHBoxLayout()
        lower_part.setAlignment(Qt.AlignmentFlag.AlignBottom)

        pinkg = icon_label("pink_g.png", 340)
        pinkg.setContentsMargins(0, 20, 0, 0)
        pinkg.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBaseline)
        
        # buttons 
        button_group = QVBoxLayout()
        button_group.setContentsMargins(0, 0, 0, 60)
        button_group.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)

        # kinder button
        self.kinder = QPushButton("KINDERGARTEN")
        self.kinder.setCursor(Qt.PointingHandCursor)
        self.kinder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.kinder.setMinimumSize(492, 86)
        self.kinder.setStyleSheet(f"""
            background-color: {YELLOW};
            font-size: 46px;
            font-family: {HEADING_FONT};
            font-weight: 800;
            color: {CORAL_RED};
            padding: 10px 10px;     
        """)
        self.kinder.clicked.connect(lambda: self.router.navigate("kindergarten"))

        # grade1 button
        self.grade1 = QPushButton("GRADE 1")
        self.grade1.setCursor(Qt.PointingHandCursor)
        self.grade1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.grade1.setMinimumSize(492, 86)
        self.grade1.setStyleSheet(f"""
            background-color: {ROSE_PINK};
            font-size: 46px;
            font-weight: 800;
            font-family: {HEADING_FONT};
            color: {YELLOW};
            padding: 10px 10px;
        """)
        self.grade1.clicked.connect(lambda: self.router.navigate("grade1_dash"))

        redb = icon_label("red_b.png", 340)
        redb.setContentsMargins(0, 20, 0, 0)
        redb.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        lower_part.addWidget(pinkg) 
        button_group.addWidget(self.kinder)
        button_group.addWidget(self.grade1)
        lower_part.addLayout(button_group)
        lower_part.addWidget(redb)
        main_layout.addLayout(lower_part)

    def showEvent(self, event):
        """Refreshes greeting and starts dashboard background music when active."""
        super().showEvent(event)
        self.refresh_teacher_greeting()
        self.play_dashboard_bgm()

    def hideEvent(self, event):
        """Stops background music when leaving the dashboard screen."""
        self.stop_dashboard_bgm()
        super().hideEvent(event)

    def play_dashboard_bgm(self):
        """Loads and plays main_dash_music.mp3 matching the current music volume setting."""
        bgm_path = os.path.join(SOUNDS_DIR, "main_dash_music.mp3")
        if os.path.exists(bgm_path):
            # Fetch current volume from AppSession (defaults or user-adjusted)
            current_vol = AppSession.get_music_volume() if hasattr(AppSession, 'get_music_volume') else 0.7
            self.audio_output.setVolume(current_vol)

            self.media_player.setSource(QUrl.fromLocalFile(os.path.abspath(bgm_path)))
            self.media_player.play()
        else:
            print(f"--> Warning: Dashboard BGM file not found at {bgm_path}")

    def stop_dashboard_bgm(self):
        """Stops the media player safely."""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.stop()

    def refresh_teacher_greeting(self):
        teacher_name = self.get_current_teacher_name()
        if hasattr(self, 'hello_text'):
            self.hello_text.setText(f"Hello, {teacher_name}!")

    def get_current_teacher_name(self):
        """Fetches the latest full_name directly from the database using AppSession or fallback."""
        try:
            teacher_id = AppSession.get_teacher_id()
            if teacher_id:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT full_name FROM teachers WHERE teacher_id = ?", (teacher_id,))
                    row = cursor.fetchone()
                    if row and row['full_name']:
                        return row['full_name']
        except Exception as e:
            print(f"--> Error fetching teacher name: {e}")

        # Fallback to latest teacher record if session ID isn't set yet
        teacher = self.get_latest_teacher()
        if teacher and teacher.get("full_name"):
            return teacher.get("full_name")

        return "Guro"

    def get_latest_teacher(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM teachers ORDER BY created_at DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    return dict(row)
        except Exception:
            pass
        return None