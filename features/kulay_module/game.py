import os
from PySide6.QtCore import Qt,QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon, QPixmap
from themes.fonts import BODY_FONT


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")

from components.cardspng import CardsPicButton
from themes.colors import *


class KulayGame(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(60, 60, 60, 0)
      
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_bar)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("pantig"))

        pagsasanay = QLabel("Pagsasanay")
        pagsasanay.setStyleSheet(f"""
                    font-size: 30px;
                    font-family: {BODY_FONT};
                    font-weight: 800;
                    color: {CHOCO_BROWN};               
                """)
        
        
        top_bar.addWidget(back_btn)
        top_bar.addWidget(pagsasanay)
        top_bar.setSpacing(20)



        draggable_items = QHBoxLayout()
        draggable_items.setSpacing(30)
        draggable_items.setAlignment(Qt.AlignmentFlag.AlignCenter)

      
        watermelon = QPixmap(os.path.join(IMAGE_DIR, "box.png")),
        turtle = QPixmap(os.path.join(IMAGE_DIR, "box.png")),
        mango = QPixmap(os.path.join(IMAGE_DIR, "box.png")),
        tree = QPixmap(os.path.join(IMAGE_DIR, "box.png"))
        
        self.setPixmap(watermelon.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setPixmap(turtle.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setPixmap(mango.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setPixmap(tree.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        draggable_items.addWidget(watermelon)
        draggable_items.addWidget(turtle)
        draggable_items.addWidget(mango)
        draggable_items.addWidget(tree)
        main_layout.addLayout(draggable_items)

        box_layout = QVBoxLayout()
        box_layout.setContentsMargins(60, 100, 60, 30)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        box = QPixmap(os.path.join(IMAGE_DIR, "box.png"))
        self.setPixmap(box.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        box_layout.addWidget(box)
        main_layout.addLayout(box_layout)
        main_layout.addStretch()



      
    