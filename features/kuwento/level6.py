import os
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import * 
from themes.fonts import BODY_FONT


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "kuwento")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "icons")



class Kuwento6(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        #top layout| back buttonnnn
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(60, 50, 0, 50)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("kuwento"))

        pagsasanay = QLabel("Kuwento 6")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(30)
        main_layout.addLayout(top_layout)

        # Title
        title = QLabel("Ang Lapis ni Dan")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 600; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        # Illustration
        image = QLabel()
        image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "ALD.png")).scaled(
                260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image)

        # Speaker icon + text row
        text_row = QHBoxLayout()
        text_row.setSpacing(15)
        text_row.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.speaker_btn = QPushButton()
        self.speaker_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "audio_icon.png")))
        self.speaker_btn.setIconSize(QSize(24, 24))
        self.speaker_btn.setFlat(True)
        self.speaker_btn.setCursor(Qt.PointingHandCursor)
        text_row.addWidget(self.speaker_btn)

        
        story_text = QLabel(
            "Matulis at matibay ang lapis ni Dan.\n"
            "Ito ay kulay dilaw na kay tingkad.\n"
            "Panulat at pangguhit na ating pangarap.\n"
            "Gumuhit ka at ito'y kulayan.\n"
            "Sumulat ka at bgkasin na tila himig sa himpapawid.\n"
            "Ito ang lapis ni Dan na puno ng pangarap."
        )
        story_text.setAlignment(Qt.AlignLeft)
        story_text.setWordWrap(True)   
        story_text.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 400;
            font-family: {BODY_FONT};
            color: {CHOCO_BROWN};
        """)
        text_row.addWidget(story_text)

        main_layout.addLayout(text_row)
        main_layout.addStretch()

        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(200)
        lower_layout.setContentsMargins(70, 20, 70, 30)
        main_layout.addLayout(lower_layout)
        
        self.next_btn = QPushButton("Sunod")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
                    background-color: {BRIGHT_YELLOW};
                    color: {CHOCO_BROWN};
                    font-size: 22px;
                    font-weight: 700;
                    border-radius: 6px;
                    font-family: {BODY_FONT};
                """)
        self.next_btn.setFixedSize(180, 50)
        lower_layout.addWidget(self.next_btn, alignment = Qt.AlignmentFlag.AlignRight)
        self.next_btn.clicked.connect(lambda: self.router.navigate("quest6"))
        
        main_layout.addStretch()

