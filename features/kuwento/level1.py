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
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "kuwento")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..","assets", "icons")


class Kuwento1(QWidget):
  def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 50, 0, 60)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("kuwento"))

   
        pagsasanay = QLabel("Kuwento 1")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        
        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(40)
        main_layout.addLayout(top_layout)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(70, 30, 70, 10)
        content_layout.setSpacing(40)
        main_layout.addLayout(content_layout)


        title = QLabel("Ang Malusog na Bata")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
                    color: {CHOCO_BROWN};
                    font-family: {BODY_FONT};
                    font-size: 40px;
                    font-weight: 800;
                """)
        content_layout.addWidget(title)


        #yung image
        content_image = QLabel()
        content_image.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "AMNB.png")).scaled(
                260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        content_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(content_image)

        #audio button and story
        text_row = QHBoxLayout()
        text_row.setSpacing(20)
        text_row.setAlignment(Qt.AlignTop)
        main_layout.addLayout(text_row)


        self.speaker_btn = QPushButton()
        self.speaker_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "audio_icon.png")))
        self.speaker_btn.setIconSize(QSize(28, 28))
        self.speaker_btn.setFlat(True)
        self.speaker_btn.setCursor(Qt.PointingHandCursor)
        text_row.addWidget(self.speaker_btn)


        content_words = QLabel( 
            "Malusog na bata si Ken.\n"
            "Uminom sya ng gatas.\n"
            "Kumakain siya ng itlog at gulay.\n"
            "Masiglang kumilos si Ken dahil malusog ang kanyang katawan."
        )
        content_words.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_words.setWordWrap(True)
        content_words.setStyleSheet(f"""
            font-family: {BODY_FONT};
            font-size: 30px;
            color: {CHOCO_BROWN};
            font-weight: 600;
        """)
        text_row.addWidget(content_words)


        main_layout.addStretch()



