import os
from PySide6.QtCore import Qt,QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from themes.fonts import BODY_FONT


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")

from components.cardspng import CardsPicButton
from themes.colors import *


class KulayScreen(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer_layout.addWidget(scroll)

        
        content = QWidget()
        main_layout = QVBoxLayout(content)
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


        pula_card = CardsPicButton ("pula.png", color = CORAL_RED) 
        pula_card.clicked.connect(lambda: self.router.navigate("pula_game"))


        kahel_card = CardsPicButton ("kahel.png", color = MARIGOLD) 
        dilaw_card = CardsPicButton ("dilaw.png", color = BRIGHT_YELLOW) 
        berde_card = CardsPicButton ("berde.png", color = GREEN)
        asul_card = CardsPicButton ("asul.png", color = CORNFLOWER_BLUE) 

        lila_card = CardsPicButton ("lila.png", color = MEDIUM_PURPLE) 
        brown_card = CardsPicButton ("tsokolate.png", color = CHOCO_BROWN) 
        itim_card = CardsPicButton ("itim.png", color = BLACK)
        

        grid_layout.addWidget(pula_card, 0, 0)
        grid_layout.addWidget(kahel_card, 0, 1)
        grid_layout.addWidget(dilaw_card, 0, 2)
        grid_layout.addWidget(berde_card, 0, 3)
        grid_layout.addWidget(asul_card, 0, 4)

        grid_layout.addWidget(lila_card, 1, 0)
        grid_layout.addWidget(brown_card, 1, 1)
        grid_layout.addWidget(itim_card, 1, 2)
 

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)
