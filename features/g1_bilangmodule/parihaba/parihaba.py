from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QIcon

from themes.colors import *
from themes.fonts import BODY_FONT
from components.lesson_card import LessonCard

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class LessonMath3(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(20)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(25)

        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent; border-radius: 6px;")
        back_btn.clicked.connect(lambda: self.router.navigate("bilang_g1"))

        pagsasanay = QLabel("Aralin: Parihaba")
        pagsasanay.setStyleSheet(f"""
            font-size: 32px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        main_layout.addLayout(top_layout)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(50)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(content_layout)

        self.content_image = QLabel()
        self.image_path = os.path.join(IMAGE_DIR, "parihaba.png")
        self.content_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.content_image)

        card = LessonCard(
            title="Aralin 4 : PARIHABA",
            body_text="Ang hugis parihaba ay may apat (4) na gilid, dalawang (2) mahaba at dalawang (2) maikli. Binubuo rin ito ng apat (4) na sulok."
        )
        content_layout.addWidget(card)

        main_layout.addStretch()

        self.speak_btn = QPushButton("Sunod ➔")
        self.speak_btn.setCursor(Qt.PointingHandCursor)
        self.speak_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BRIGHT_YELLOW};
                color: {CHOCO_BROWN};
                font-size: 22px;
                font-weight: 800;
                border-radius: 14px;
                padding: 14px 35px;
                font-family: {BODY_FONT};
            }}
            QPushButton:hover {{
                background-color: #F1C40F;
            }}
        """)
        self.speak_btn.clicked.connect(lambda: self.router.navigate("parihaba_quest"))
        
        main_layout.addWidget(self.speak_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.update_responsive_scaling()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_responsive_scaling()

    def update_responsive_scaling(self):
        screen_width = self.width()
        screen_height = self.height()
        
        scale_factor = min(screen_width, screen_height)
        img_size = int(scale_factor * 0.38)
        img_size = max(250, min(img_size, 550))

        if os.path.exists(self.image_path):
            self.content_image.setPixmap(QPixmap(self.image_path).scaled(
                img_size, img_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))