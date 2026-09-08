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


class SalitaScreen(QWidget):
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

        #Lesson: Pang-uri
        lvl1 = GridButton ("1", color = CORAL_RED)
        lvl1.clicked.connect(lambda: self.router.navigate("salita1"))

        lvl2 = GridButton ("2", color = MARIGOLD)
        lvl2.clicked.connect(lambda: self.router.navigate("salitaq1"))

        lvl3 = GridButton ("3", color = ELECTRIC_VIOLET) 
        lvl3.clicked.connect(lambda: self.router.navigate("salitaq2"))

        lvl4 = GridButton ("4", color = HOT_PINK)
        lvl4.clicked.connect(lambda: self.router.navigate("salitaq3"))

        lvl5 = GridButton ("5", color = SKY_BLUE)
        lvl5.clicked.connect(lambda: self.router.navigate("salitaq4"))
         

        lvl6 = GridButton ("6", color = LIGHT_GREEN)
        lvl6.clicked.connect(lambda: self.router.navigate("salita2"))

        lvl7 = GridButton ("7", color = COBALT_BLUE)
        lvl7.clicked.connect(lambda: self.router.navigate("salitaq5"))

        lvl8 = GridButton ("8", color = TERRACOTTA)
        lvl8.clicked.connect(lambda: self.router.navigate("salitaq6"))

        lvl9 = GridButton ("9", color = BURNT_ORANGE)
        lvl9.clicked.connect(lambda: self.router.navigate("salitaq7"))

        lvl10 = GridButton ("10", color = MAGENTA)
        lvl10.clicked.connect(lambda: self.router.navigate("salitaq8"))


        lvl11 = GridButton ("11", color = CORAL_RED)
        lvl11.clicked.connect(lambda: self.router.navigate("salita3"))

        lvl12 = GridButton ("12", color = MARIGOLD)
        lvl12.clicked.connect(lambda: self.router.navigate("salitaq1"))

        lvl13 = GridButton ("13", color = ELECTRIC_VIOLET) 
        lvl13.clicked.connect(lambda: self.router.navigate("salitaq2"))

        lvl14 = GridButton ("14", color = HOT_PINK)
        lvl14.clicked.connect(lambda: self.router.navigate("salitaq3"))

        lvl15 = GridButton ("15", color = SKY_BLUE)
        lvl15.clicked.connect(lambda: self.router.navigate("salitaq4"))
 
         

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

        grid_layout.addWidget(lvl11, 2, 0)
        grid_layout.addWidget(lvl12, 2, 1)
        grid_layout.addWidget(lvl13, 2, 2)
        grid_layout.addWidget(lvl14, 2, 3)
        grid_layout.addWidget(lvl15, 2, 4)



        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        scroll.setWidget(content)
