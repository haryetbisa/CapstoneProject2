from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from themes.fonts import HEADING_FONT, BODY_FONT
from components.cardspng import CardsPicButton
from themes.colors import *

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


class HugisScreen(QWidget):
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
        back_btn.clicked.connect(lambda: self.router.navigate("kindergarten"))

   
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


        bilog_card = CardsPicButton("bilog.png", color = CORAL_RED)
        bilog_card.clicked.connect(lambda: self.router.navigate("lesson"))

        tatsu_card = CardsPicButton("tatsulok.png", color = MARIGOLD)
        parisukat_card = CardsPicButton("parisukat.png", color = ELECTRIC_VIOLET) 
        puso_card = CardsPicButton("puso.png", color = HOT_PINK)
        oblong_card = CardsPicButton("oblong.png", color = SKY_BLUE) 
        parihaba_card = CardsPicButton("parihaba.png", color = LIGHT_GREEN)
        bituin_card = CardsPicButton("bituin.png", color = COBALT_BLUE) 
        rombus_card = CardsPicButton("brilyante.png", color = TERRACOTTA )

        hugis_cards = [bilog_card, tatsu_card, puso_card, oblong_card, parihaba_card, bituin_card, rombus_card]

        def connect_screen():
            self.router.navigate("lesson")
        
        for cards in hugis_cards:
            cards.clicked.connect(connect_screen)
        
        grid_layout.addWidget(bilog_card, 0, 0)
        grid_layout.addWidget(tatsu_card, 0, 1)
        grid_layout.addWidget(parisukat_card, 0, 2)
        grid_layout.addWidget(puso_card, 0, 3)
        grid_layout.addWidget(oblong_card, 0, 4)
        grid_layout.addWidget(parihaba_card, 1, 0)
        grid_layout.addWidget(bituin_card, 1, 1)
        grid_layout.addWidget(rombus_card, 1, 2)


        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
