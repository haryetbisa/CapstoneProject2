from assets.icon import icon_label
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QTransform
from themes.colors import *
from themes.fonts import BODY_FONT
from themes.colors import *

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


class CreateAccount(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(300)
        main_layout.addLayout(top_layout)


        #LEFT TOP KID
        left_top = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "yellow_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap = pixmap.transformed(QTransform().rotate(0), Qt.SmoothTransformation)
        left_top.setPixmap(pixmap)
        left_top.move(-160, -20)   
        left_top.show()
        top_layout.addWidget(left_top)


        #logo
        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "logoo.png")).scaled(
                400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(logo)


        #RIGHT TOP KID
        right_top = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "red_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap = pixmap.transformed(QTransform().rotate(0), Qt.SmoothTransformation)
        right_top.setPixmap(pixmap)
        right_top.move(200, -20)   # ← tweak these two numbers until it looks right
        right_top.show()
        top_layout.addWidget(right_top)

        main_layout.addStretch()

        subtitle =QLabel("Teachers learning tools for students,\nfor practicing basic Filipino reading and basic Math.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {CHOCO_BROWN}; font-size: 22px; font-weight: 500; font-family: {BODY_FONT};")
        main_layout.addWidget(subtitle)

        main_layout.addStretch()

        create_btn = QPushButton("Create account")
        create_btn.setStyleSheet(f"background-color: {CORAL_RED}; color: {LIGHT}; font-size: 20px; font-weight: 600px; font-family: {BODY_FONT}; border-radius: 6px;")
        create_btn.clicked.connect(lambda: self.router.navigate("credentials"))
        create_btn.setFixedSize(300,50)
        main_layout.addWidget(create_btn, alignment = Qt.AlignmentFlag.AlignCenter)


        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.setSpacing(1000)
        bottom_layout.setContentsMargins(0, 10, 0, 0)


        #LEFT BOTTOM KID
        left_bottom = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "blue_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap = pixmap.transformed(QTransform().rotate(0), Qt.SmoothTransformation)
        left_bottom.setPixmap(pixmap)
        left_bottom.move(-100, -60)   # ← tweak these two numbers until it looks right
        left_bottom.show()
        bottom_layout.addWidget(left_bottom)


        #RIGHT BOTTOM KID
        right_bottom = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "pink_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap = pixmap.transformed(QTransform().rotate(0), Qt.SmoothTransformation)
        right_bottom.setPixmap(pixmap)
        right_bottom.move(200, -60)   # ← tweak these two numbers until it looks right
        right_bottom.show()
        bottom_layout.addWidget(right_bottom)


        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()
        
        

        

