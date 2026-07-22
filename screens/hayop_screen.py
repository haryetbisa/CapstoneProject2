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


class HayopScreen(QWidget):
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


        aso_card = CardsPicButton ("aso.png", color = CORAL_RED) 
        baboy_card = CardsPicButton ("baboy.png", color = MARIGOLD) 
        isda_card = CardsPicButton ("isda.png", color = ELECTRIC_VIOLET) 
        kalabaw_card = CardsPicButton ("kalabaw.png", color = HOT_PINK)
        kabayo_card = CardsPicButton ("kabayo.png", color = SKY_BLUE) 

        pagong_card = CardsPicButton ("pagong.png", color = LIGHT_GREEN) 
        tarsier_card = CardsPicButton ("tarsier.png", color = COBALT_BLUE) 
        agila_card = CardsPicButton ("agila.png", color = TERRACOTTA) 
        bibe_card = CardsPicButton ("bibe.png", color = BURNT_ORANGE) 
        manok_card = CardsPicButton ("manok.png", color = MAGENTA) 

        unggoy_card = CardsPicButton ("unggoy.png", color = CORAL_RED) 
        elepante_card = CardsPicButton ("elepante.png", color = MARIGOLD) 
        kambing_card = CardsPicButton ("kambing.png", color = ELECTRIC_VIOLET) 
        palaka_card = CardsPicButton ("palaka.png", color = HOT_PINK) 
        kuneho_card = CardsPicButton ("kuneho.png", color = SKY_BLUE) 
        

        grid_layout.addWidget(aso_card, 0, 0)
        grid_layout.addWidget(baboy_card, 0, 1)
        grid_layout.addWidget(isda_card, 0, 2)
        grid_layout.addWidget(kalabaw_card, 0, 3)
        grid_layout.addWidget(kabayo_card, 0, 4)

        grid_layout.addWidget(pagong_card, 1, 0)
        grid_layout.addWidget(tarsier_card, 1, 1)
        grid_layout.addWidget(agila_card, 1, 2)
        grid_layout.addWidget(bibe_card, 1, 3)
        grid_layout.addWidget(manok_card, 1, 4)

        grid_layout.addWidget(unggoy_card, 2, 0)
        grid_layout.addWidget(elepante_card, 2, 1)
        grid_layout.addWidget(kambing_card, 2, 2)
        grid_layout.addWidget(palaka_card, 2, 3)
        grid_layout.addWidget(kuneho_card, 2, 4)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)
