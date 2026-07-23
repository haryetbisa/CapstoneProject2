
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QMovie
from themes.colors import *
from themes.fonts import BODY_FONT
from themes.colors import *

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")
GIF_DIR = os.path.join(BASE_DIR, "..", "assets", "gif")

class LoadingScreen(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 100, 0, 0)
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(300)
        top_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(top_layout)

        left_top = QLabel()
        left_top.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "pink_g.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        left_top.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(left_top)


        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "logo.png")).scaled(
                400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(logo)


        right_top = QLabel()
        right_top.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "red_b.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        right_top.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(right_top)


        subtitle =QLabel("Kids reading assistant\nfor practicing early reading ")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {CHOCO_BROWN}; font-size: 22px; font-weight: 300px; font-family: {BODY_FONT};")
        main_layout.addWidget(subtitle)

        self.loading_gif = QLabel()
        self.loading_gif.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.loading_gif)

        self.movie = QMovie(os.path.join(GIF_DIR, "loading_gif.gif"))
        self.loading_gif.setMovie(self.movie)
        self.movie.start()

        def next_screen():
          self.movie.stop()
          self.router.navigate("createacc")
    
        QTimer.singleShot(10000, next_screen)


        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.setSpacing(1000)
        bottom_layout.setContentsMargins(0, 10, 0, 0)

        left_bottom = QLabel()
        left_bottom.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "pink_g.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        left_bottom.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        bottom_layout.addWidget(left_bottom)


        right_bottom = QLabel()
        right_bottom.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "red_b.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        right_bottom.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        bottom_layout.addWidget(right_bottom)


        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()
        
        

        

