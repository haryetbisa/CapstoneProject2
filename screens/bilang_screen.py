from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide6.QtGui import QIcon
from themes.fonts import HEADING_FONT, BODY_FONT
from components.grid_btn import GridButton
from themes.colors import *

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


class BilangScreen(QWidget):
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


        one_card = GridButton ("1", color = CORAL_RED)
        one_card.clicked.connect(lambda: self.router.navigate("1"))

        two_card = GridButton ("2", color = MARIGOLD)
        two_card.clicked.connect(lambda: self.router.navigate("2"))

        three_card = GridButton ("3", color = ELECTRIC_VIOLET) 
        three_card.clicked.connect(lambda: self.router.navigate("3"))

        four_card = GridButton ("4", color = HOT_PINK)
        four_card.clicked.connect(lambda: self.router.navigate("4"))

        five_card = GridButton ("5", color = SKY_BLUE)
        five_card.clicked.connect(lambda: self.router.navigate("5"))
         

        six_card = GridButton ("6", color = LIGHT_GREEN)
        six_card.clicked.connect(lambda: self.router.navigate("6"))

        seven_card = GridButton ("7", color = COBALT_BLUE) 
        seven_card.clicked.connect(lambda: self.router.navigate("7"))

        eight_card = GridButton ("8", color = TERRACOTTA) 
        eight_card.clicked.connect(lambda: self.router.navigate("8"))

        nine_card = GridButton ("9", color = BURNT_ORANGE)
        nine_card.clicked.connect(lambda: self.router.navigate("9"))

        ten_card = GridButton ("10", color = MAGENTA)
        ten_card.clicked.connect(lambda: self.router.navigate("10"))
         

        grid_layout.addWidget(one_card, 0, 0)
        grid_layout.addWidget(two_card, 0, 1)
        grid_layout.addWidget(three_card, 0, 2)
        grid_layout.addWidget(four_card, 0, 3)
        grid_layout.addWidget(five_card, 0, 4)

        grid_layout.addWidget(six_card, 1, 0)
        grid_layout.addWidget(seven_card, 1, 1)
        grid_layout.addWidget(eight_card, 1, 2)
        grid_layout.addWidget(nine_card, 1, 3)
        grid_layout.addWidget(ten_card, 1, 4)


        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)
