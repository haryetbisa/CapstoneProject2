
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QProgressBar
from PySide6.QtGui import QPixmap
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
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #logo
        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "logoo.png")).scaled(
                500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo)


        subtitle =QLabel("A Filipino-based basic words and basic math learning tool\nfor teachers in Kindergarten and Grade 1.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {CHOCO_BROWN}; font-size: 22px; font-weight: 500; font-family: {BODY_FONT};")
        main_layout.addWidget(subtitle)


#Loading Widget
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(300, 20)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #F0E9D8;
                border-radius: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {HONEY_YELLOW};
                border-radius: 10px;
            }}
        """)
        main_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

 
        # ---- Animate the progress bar from 0 to 100 over 3 seconds ----
        self.animation = QPropertyAnimation(self.progress_bar, b"value")
        self.animation.setDuration(10000)          # 3000ms = 3 seconds
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)   # smooth acceleration/deceleration
        self.animation.finished.connect(self.go_to_next_screen)
        self.animation.start()

#Bottom Layout (kids)
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.setSpacing(20)
        bottom_layout.setContentsMargins(0, 10, 0, 0)

        left_bottom = QLabel()
        left_bottom.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "hugis.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        left_bottom.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        bottom_layout.addWidget(left_bottom)

        left_top = QLabel()
        left_top.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "Pangungusap.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        left_top.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        bottom_layout.addWidget(left_top)

        
        right_top = QLabel()
        right_top.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "kulay.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        right_top.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        bottom_layout.addWidget(right_top)


        right_bottom = QLabel()
        right_bottom.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "kuwento.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        right_bottom.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        bottom_layout.addWidget(right_bottom)

        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()


    def go_to_next_screen(self):
                self.router.navigate("createacc")
 

 


        



        
        

        

