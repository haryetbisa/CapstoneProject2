import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import * 
from themes.fonts import BODY_FONT
from components.choices_button import ChoicesButton


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")



class BilangLvl3(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(40)

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
        back_btn.clicked.connect(lambda: self.router.navigate("g1_parihaba"))

        pagsasanay = QLabel("Pagsasanay: Parihaba")
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

        #question
        title = QLabel("Ilan ang gilid at sulok ng hugis parihaba?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 800; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        # Illustration
        image = QLabel()
        image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "parihaba.png")).scaled(
                200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image)

        #choices
        quest_row = QHBoxLayout()
        quest_row.setSpacing(29)
        quest_row.setAlignment(Qt.AlignCenter)

        self.opt_1 = ChoicesButton("3", color = SKY_BLUE)
        self.opt_2 = ChoicesButton("4", color = HOT_PINK) #tamang sagot
        self.opt_3 = ChoicesButton("5", color = LIGHT_GREEN) 

        quest_row.addWidget(self.opt_1)
        quest_row.addWidget(self.opt_2)
        quest_row.addWidget(self.opt_3)

        main_layout.addLayout(quest_row)
        main_layout.addStretch()

