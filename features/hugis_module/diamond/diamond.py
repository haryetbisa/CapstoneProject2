from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPushButton, QLineEdit
from PySide6.QtGui import QPixmap, QIcon


from components.cardsbutton import CardsButton
from themes.colors import *
from assets.icon import icon_label
from themes.fonts import  BODY_FONT
from components.lesson_card import LessonCard

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..","..", "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class LessonScreenDiamond(QWidget):
  def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60,60,60,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("hugis"))

   
        pagsasanay = QLabel("Aralin: Rombus")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        
        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(50)
        main_layout.addLayout(top_layout)



        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(70, 30, 70, 30)
        content_layout.setSpacing(280)
        main_layout.addLayout(content_layout)

        #yung image
        content_image = QLabel()
        content_image.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "brilyante.png")).scaled(
                450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        content_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(content_image)

        #lesson explanation
        card = LessonCard(
        title="Aralin 8 : ROMBUS",
        body_text="Ang hugis rombus ay mas kilala na dayamond. Ito ay may apat na gilid na maihahalintulad sa hugis ng saranggola.")
        content_layout.addWidget(card)

        self.speak_btn = QPushButton("Sunod")
        self.speak_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "mic_icon.png")))
        self.speak_btn.setIconSize(QSize(30, 30))
        self.speak_btn.setFixedHeight(40)
        self.speak_btn.setCursor(Qt.PointingHandCursor)
        self.speak_btn.setStyleSheet(f"""
            background-color: {BRIGHT_YELLOW};
            color: {CHOCO_BROWN};
            font-size: 22px;
            font-weight: 800;
            border-radius: 6px;
            font-family: {BODY_FONT};
        """)
        self.speak_btn.setFixedSize(240, 70)
        main_layout.addWidget(self.speak_btn, alignment = Qt.AlignmentFlag.AlignRight)
        self.speak_btn.clicked.connect(lambda: self.router.navigate("diamondvs"))



        main_layout.addLayout(content_layout)
        main_layout.addStretch()


