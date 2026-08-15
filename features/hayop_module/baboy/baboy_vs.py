# screens/home_screen.py
import os

from assets.icon import icon_label
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from themes.colors import *
from themes.fonts import BODY_FONT


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..","..", "..", "assets", "icons")

class BaboyVS(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router


        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)

        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_bar)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("baboy_lesson"))

   
        pagsasanay = QLabel("Pagsasanay")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};               
        """)


        top_bar.addWidget(back_btn)
        top_bar.addWidget(pagsasanay)
        top_bar.setSpacing(20)


        image = QLabel()
        image.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "baboy.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(image)


        word = QHBoxLayout()
        word.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word.setSpacing(20)

        self.audio = QPushButton()
        self.audio.setIcon(QIcon(os.path.join(ICONS_DIR, "audio_icon.png")))
        self.audio.setIconSize(QSize(40, 40))
        self.audio.setCursor(Qt.PointingHandCursor)
        word.addWidget(self.audio)
        

        salita = QLabel("Ba-boy")
        salita.setStyleSheet(f"""
            font-size: 96px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};               
        """)
        word.addWidget(salita)

        main_layout.addLayout(word)


        self.speak_btn = QPushButton("I-TAP KAPAG MAG-SASALITA")
        self.speak_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "mic_icon.png")))
        self.speak_btn.setIconSize(QSize(30, 30))
        self.speak_btn.setFixedHeight(50)
        self.speak_btn.setCursor(Qt.PointingHandCursor)
        self.speak_btn.setStyleSheet(f"""
            background-color: {BRIGHT_YELLOW};
            color: {CHOCO_BROWN};
            font-size: 20px;
            font-weight: 500;
            border-radius: 6px;
            font-family: {BODY_FONT};
        """)
        self.speak_btn.setFixedSize(554, 70)
        main_layout.addWidget(self.speak_btn, alignment = Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(40)
        main_layout.addStretch(3)




      


