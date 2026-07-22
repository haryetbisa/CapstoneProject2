import os
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon


from components.cardsbutton import CardsButton
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


class KinderDashboard(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)
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
        back_btn.clicked.connect(lambda: self.router.navigate("home"))
        main_layout.setAlignment(back_btn, Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(back_btn)

        title = QLabel("KINDERGARTEN DASHBOARD")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 40px;
            font-family: {HEADING_FONT};
            font-weight: 900;
            color: {CHOCO_BROWN};
        """)
        top_layout.addWidget(title)
        top_layout.setSpacing(100)


        grid_layout = QGridLayout()
        grid_layout.setSpacing(50)        
        grid_layout.setContentsMargins(0, 50, 0, 0)


        pantig_card = CardsButton("Pantig", "pantig.png", color = LIGHT_GREEN)
        pantig_card.clicked.connect(lambda: self.router.navigate("pantig"))

        bilang_card = CardsButton("Bilang", "Bilang.png", color = MAGENTA)
        bilang_card.clicked.connect(lambda: self.router.navigate("bilang"))

        hugis_card = CardsButton("Hugis", "hugis.png", color = ORCHID_PINK) 
        hugis_card.clicked.connect(lambda: self.router.navigate("hugis"))

        parte_card = CardsButton("Parte ng Katawan", "parte.png", color = SKY_BLUE)
        parte_card.clicked.connect(lambda: self.router.navigate("katawan"))

        kulay_card = CardsButton("Kulay", "kulay.png", color = LIGHT_CORAL_PINK) 
        kulay_card.clicked.connect(lambda: self.router.navigate("kulay"))

        hayop_card = CardsButton("Hayop", "hayop.png", color = COBALT_BLUE) 
        hayop_card.clicked.connect(lambda: self.router.navigate("hayop"))


        grid_layout.addWidget(pantig_card, 0, 0)
        grid_layout.addWidget(bilang_card, 0, 1)
        grid_layout.addWidget(hugis_card, 0, 2)
        grid_layout.addWidget(parte_card, 1, 0)
        grid_layout.addWidget(kulay_card, 1, 1)
        grid_layout.addWidget(hayop_card, 1, 2)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
