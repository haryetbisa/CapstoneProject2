from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon

from components.cardsbutton import CardsButton
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")



class GradeOneDashboard(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(60, 60, 60, 0)
        
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("home"))
        main_layout.setAlignment(back_btn, Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(back_btn)

        title = QLabel("GRADE 1 DASHBOARD")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 40px;
            font-family: {HEADING_FONT};
            font-weight: 900;
            color: {CHOCO_BROWN};
        """)
        top_layout.addWidget(title)
        top_layout.setSpacing(130)
        main_layout.addLayout(top_layout)

        main_layout.addSpacing(40)
        grid_layout =QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)     
        grid_layout.setContentsMargins(0, 50, 0, 0)

        bilang_card = CardsButton("Bilang", "Bilang.png", color = LIGHT_GREEN)
        bilang_card.clicked.connect(lambda: self.router.navigate("bilang_g1"))

        pangungusap = CardsButton("Pangungusap", "Pangungusap.png", color = MAGENTA)
        pangungusap.clicked.connect(lambda: self.router.navigate("bilang_g1"))

        kuwento_card = CardsButton("Kuwento", "kuwento.png", color = ORCHID_PINK)
        kuwento_card.clicked.connect(lambda: self.router.navigate("kuwento"))
        
        grid_layout.addWidget(bilang_card, 0, 0)
        grid_layout.addWidget(pangungusap, 0, 1)
        grid_layout.addWidget(kuwento_card, 0, 2)
      

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
