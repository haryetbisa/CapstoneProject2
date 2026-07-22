from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from themes.fonts import HEADING_FONT, BODY_FONT

from components.cardsbutton import CardsButton
from themes.colors import *

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")

class KuwentoScreen(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60,60,60,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("grade1_dash"))

   
        pagsasanay = QLabel("Pagsasanay")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(20)


        grid_layout =QGridLayout()
        grid_layout.setSpacing(50)        
        grid_layout.setContentsMargins(0, 50, 0, 0)


        lvl1 = CardsButton("Bilog", "bilog.png", color = CORAL_RED)
        lvl2 = CardsButton("Tatsulok", "tatsulok.png", color = MARIGOLD)
        lvl3 = CardsButton("Parisukat", "parisukat.png", color = ELECTRIC_VIOLET) 
        lvl4 = CardsButton("Puso", "puso.png", color = HOT_PINK)
        lvl5 = CardsButton("Bilohaba", "oblong.png", color = SKY_BLUE) 
        lvl6 = CardsButton("Parihaba", "parihaba.png", color = LIGHT_GREEN)
        lvl7 = CardsButton("Bituin", "bituin.png", color = COBALT_BLUE) 
        lvl8 = CardsButton("Rombus", "brilyante.png", color = TERRACOTTA )
        lvl9 = CardsButton("Rombus", "brilyante.png", color = DARK_YELLOW )
        lvl10 = CardsButton("Rombus", "brilyante.png", color = MAGENTA )
        
        grid_layout.addWidget(lvl1, 0, 0)
        grid_layout.addWidget(lvl2, 0, 1)
        grid_layout.addWidget(lvl3, 0, 2)
        grid_layout.addWidget(lvl4, 0, 3)
        grid_layout.addWidget(lvl5, 0, 4)
        grid_layout.addWidget(lvl6, 1, 0)
        grid_layout.addWidget(lvl7, 1, 1)
        grid_layout.addWidget(lvl8, 1, 2)
        grid_layout.addWidget(lvl9, 1, 3)
        grid_layout.addWidget(lvl10, 1, 4)


        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
