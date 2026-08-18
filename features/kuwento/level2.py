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
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..","assets", "image_content", "kuwento")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "icons")


class Kuwento2(QWidget):
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
        back_btn.clicked.connect(lambda: self.router.navigate("kuwento"))

   
        pagsasanay = QLabel("Ang Aking Alaga")
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



        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(70, 30, 70, 30)
        content_layout.setSpacing(280)
        main_layout.addLayout(content_layout)


        title = QLabel("Ang Aking Alaga")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
                    color: {CHOCO_BROWN};
                    font-family: {BODY_FONT};
                    font-size: 30px;
                    font-weight: 600;
                """)
        content_layout.addWidget(title)


        #yung image
        content_image = QLabel()
        content_image.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "AAA.png")).scaled(
                450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation
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
        self.speaker_btn.setIconSize(QSize(24, 24))
        self.speaker_btn.setFlat(True)
        self.speaker_btn.setCursor(Qt.PointingHandCursor)
        text_row.addWidget(self.speaker_btn)


        content_words = QLabel( 
            "Ako ay may alaga.\n"
            "Masipag manghuli ng daga.\n"
            "Binibigyan ko siya ng isda.\n"
            "Siya ang mahal kong pusa."
        )
        content_words.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_words.setStyleSheet(f"""
            font-family: {BODY_FONT};
            font-size: 20px;
            color: {CHOCO_BROWN};
            font-weight: 400;
        """)
        text_row.addWidget(content_words)



