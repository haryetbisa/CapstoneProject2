#back arrow nav

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QColor
from themes.colors import *
from assets.icon import icon_label

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "assets", "image"))

class BackButton(QPushButton):
    def __init__(self, color = "gray", parent = None):
        super().__init__()

        base = QColor(color)
        hover_color = base.lighter(115).name()  
        pressed_color = base.darker(115).name()


        self.setFixedSize(60, 40)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};           
                border: none;
                border-radius: 22px;                 
            }}
            QPushButton:hover {{
                background-color: {hover_color};         
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};         
            }}
        """)

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(15, 25, 15, 20)                        
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.image_label = icon_label("back_arrow.png", 30)
     
        
      
        