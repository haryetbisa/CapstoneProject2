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

class PantigScreen(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(60, 60, 60, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet =(f"""
        QScrollArea {{
            border: none;
        }}

        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
            margin: 0px;
        }}

        QScrollBar::handle:vertical {{
            background: {BLACK};
            border-radius: 5px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {BLACK};
        }}
        """) 
       
        outer_layout.addWidget(scroll)

        
        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(20,20,20,20)
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


        A_card = GridButton ("A", color = CORAL_RED)
        A_card.clicked.connect(lambda: self.router.navigate("vr"))

        Ba_card = GridButton ("BA", color = MARIGOLD) 
        Ka_card = GridButton ("KA", color = ELECTRIC_VIOLET) 
        Da_card = GridButton ("DA", color = HOT_PINK)
        E_card = GridButton ("E", color = SKY_BLUE) 

        Ga_card = GridButton ("GA", color = LIGHT_GREEN) 
        Ha_card = GridButton ("HA", color = COBALT_BLUE) 
        I_card = GridButton ("I", color = TERRACOTTA) 
        La_card = GridButton ("LA", color = BURNT_ORANGE)
        Ma_card = GridButton ("MA", color = MAGENTA)

        Na_card = GridButton ("NA", color = CORAL_RED) 
        Nga_card = GridButton ("NGA", color = MARIGOLD) 
        O_card = GridButton ("O", color = ELECTRIC_VIOLET) 
        Pa_card = GridButton ("PA", color = HOT_PINK)
        Ra_card = GridButton ("RA", color = SKY_BLUE)   

        Sa_card = GridButton ("SA", color = LIGHT_GREEN) 
        Ta_card = GridButton ("TA", color = COBALT_BLUE) 
        U_card = GridButton ("U", color = TERRACOTTA) 
        Wa_card = GridButton ("WA", color = BURNT_ORANGE)
        Ya_card = GridButton ("YA", color = MAGENTA)    
         

        grid_layout.addWidget(A_card, 0, 0)
        grid_layout.addWidget(Ba_card, 0, 1)
        grid_layout.addWidget(Ka_card, 0, 2)
        grid_layout.addWidget(Da_card, 0, 3)
        grid_layout.addWidget(E_card, 0, 4)

        grid_layout.addWidget(Ga_card, 1, 0)
        grid_layout.addWidget(Ha_card, 1, 1)
        grid_layout.addWidget(I_card, 1, 2)
        grid_layout.addWidget(La_card, 1, 3)
        grid_layout.addWidget(Ma_card, 1, 4)

        grid_layout.addWidget(Na_card, 2, 0)
        grid_layout.addWidget(Nga_card, 2, 1)
        grid_layout.addWidget(O_card, 2, 2)
        grid_layout.addWidget(Pa_card, 2, 3)
        grid_layout.addWidget(Ra_card, 2, 4)

        grid_layout.addWidget(Sa_card, 3, 0)
        grid_layout.addWidget(Ta_card, 3, 1)
        grid_layout.addWidget(U_card, 3, 2)
        grid_layout.addWidget(Wa_card, 3, 3)
        grid_layout.addWidget(Ya_card, 3, 4)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)

        def clicked():
            A_card.clicked.connect(lambda: self.router.navigate("vr"))

