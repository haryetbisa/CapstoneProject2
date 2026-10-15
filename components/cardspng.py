#para sa grid layout na content na may png/icon lang omsim

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QPixmap, QColor
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "assets", "image"))

class CardsPicButton(QPushButton):
    def __init__(self, icon_path, color = "gray", font_family= "Arial", parent = None):
        super().__init__()

        base = QColor(color)
        hover_color = base.lighter(115).name()  
        pressed_color = base.darker(115).name()


        self.setFixedSize(206, 224)
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
        card_layout.setSpacing(20)                      
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.aralin = QLabel("Aralin:")
        self.aralin.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.aralin.setStyleSheet(f"""
                    color: {WHITE};
                    font-family: {BODY_FONT};
                    font-size: 16px;
                    font-weight: 500;
                    background: transparent;
                """)


        self.image_label = QLabel()
        self.image_label.setStyleSheet("background: transparent;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(QPixmap(os.path.join(ASSETS_DIR, icon_path)).scaled(
                140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        

        card_layout.addWidget(self.aralin)
        card_layout.addWidget(self.image_label)
     
        