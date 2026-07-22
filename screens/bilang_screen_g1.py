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

class BilangScreenG1(QWidget):
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


        one_card = GridButton ("1", color = CORAL_RED) 
        two_card = GridButton ("2", color = MARIGOLD) 
        three_card = GridButton ("3", color = ELECTRIC_VIOLET) 
        four_card = GridButton ("4", color = HOT_PINK)
        five_card = GridButton ("5", color = SKY_BLUE) 

        six_card = GridButton ("6", color = LIGHT_GREEN) 
        seven_card = GridButton ("7", color = COBALT_BLUE) 
        eight_card = GridButton ("8", color = TERRACOTTA) 
        nine_card = GridButton ("9", color = BURNT_ORANGE)
        ten_card = GridButton ("10", color = MAGENTA)

        card11 = GridButton ("11", color = LIGHT_GREEN) 
        card12= GridButton ("12", color = COBALT_BLUE) 
        card13 = GridButton ("13", color = TERRACOTTA) 
        card14 = GridButton ("14", color = BURNT_ORANGE)
        card15 = GridButton ("15", color = MAGENTA)   

        card16 = GridButton ("16", color = LIGHT_GREEN) 
        card17= GridButton ("17", color = COBALT_BLUE) 
        card18 = GridButton ("18", color = TERRACOTTA) 
        card19 = GridButton ("19", color = BURNT_ORANGE)
        card20 = GridButton ("20", color = MAGENTA)  
        
         

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

        grid_layout.addWidget(card11, 2, 0)
        grid_layout.addWidget(card12, 2, 1)
        grid_layout.addWidget(card13, 2, 2)
        grid_layout.addWidget(card14, 2, 3)
        grid_layout.addWidget(card15, 2, 4)

        grid_layout.addWidget(card16, 3, 0)
        grid_layout.addWidget(card17, 3, 1)
        grid_layout.addWidget(card18, 3, 2)
        grid_layout.addWidget(card19, 3, 3)
        grid_layout.addWidget(card20, 3, 4)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)
