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
IMAGE_DIR = os.path.join(BASE_DIR, "..","..", "..", "assets", "image_content", "kulay")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class Dilaw(QWidget):
  def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 50, 0, 60)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("kulay"))

   
        pagsasanay = QLabel("Aralin: Dilaw")
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
        content_image.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "dilaw.png")).scaled(
                450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        content_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(content_image)

        #lesson explanation
        card = LessonCard(
        title="Aralin 3 : DILAW",
        body_text="Ang kulay Dilaw ay isa sa mga pangunahing kulay. Sumisimbolo ito ng liwanag ng araw at kasiyahan. Madalas itong makikita sa mga hinog na prutas kagaya ng saging, mangga, at pinya. Makikita din ang kulay na ito sa mga hayop at bulaklak kagaya ng sisiw, ibon, at sunflower.")
        content_layout.addWidget(card)

        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(200)
        lower_layout.setContentsMargins(70, 20, 70, 30)
        main_layout.addLayout(lower_layout)

        audio_btn = QLabel()
        audio_btn.setPixmap(QPixmap(os.path.join(ICONS_DIR, "play.png")).scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        audio_btn.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        lower_layout.addWidget(audio_btn)

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
        lower_layout.addWidget(self.speak_btn, alignment = Qt.AlignmentFlag.AlignRight)
        self.speak_btn.clicked.connect(lambda: self.router.navigate("dilaw_game"))
