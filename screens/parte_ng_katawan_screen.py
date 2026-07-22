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


class ParteNgKatawanScreen(QWidget):
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


        mata_card = CardsPicButton ("giraffe.png", color = CORAL_RED) 
        ilong_card = CardsPicButton ("giraffe.png", color = MARIGOLD) 
        bibig_card = CardsPicButton ("giraffe.png", color = ELECTRIC_VIOLET) 
        tainga_card = CardsPicButton ("giraffe.png", color = HOT_PINK)
        ulo_card = CardsPicButton ("giraffe.png", color = SKY_BLUE) 

        leeg_card = CardsPicButton ("giraffe.png", color = LIGHT_GREEN) 
        balikat_card = CardsPicButton ("giraffe.png", color = COBALT_BLUE) 
        tiyan_card = CardsPicButton ("giraffe.png", color = TERRACOTTA) 
        braso_card = CardsPicButton ("giraffe.png", color = BURNT_ORANGE) 
        kamay_card = CardsPicButton ("giraffe.png", color = MAGENTA) 

        binti_card = CardsPicButton ("giraffe.png", color = CORAL_RED) 
        tuhod_card = CardsPicButton ("giraffe.png", color = MARIGOLD) 
        paa_card = CardsPicButton ("giraffe.png", color = ELECTRIC_VIOLET) 
        
        

        grid_layout.addWidget(mata_card, 0, 0)
        grid_layout.addWidget(ilong_card, 0, 1)
        grid_layout.addWidget(bibig_card, 0, 2)
        grid_layout.addWidget(tainga_card, 0, 3)
        grid_layout.addWidget(ulo_card, 0, 4)

        grid_layout.addWidget(leeg_card, 1, 0)
        grid_layout.addWidget(balikat_card, 1, 1)
        grid_layout.addWidget(tiyan_card, 1, 2)
        grid_layout.addWidget(braso_card, 1, 3)
        grid_layout.addWidget(kamay_card, 1, 4)

        grid_layout.addWidget(binti_card, 2, 0)
        grid_layout.addWidget(tuhod_card, 2, 1)
        grid_layout.addWidget(paa_card, 2, 2)
 

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)
