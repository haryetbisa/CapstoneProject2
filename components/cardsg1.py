# para sa dashboard buttons na may png at words


import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QColor
from themes.colors import *
from assets.image import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "assets", "image_content", "kuwento"))

class CardsButtonG1(QPushButton):
    def __init__(self, title_text, icon_path = "giraffe.png", color = "gray", font_family= "Poppins", parent = None):
        super().__init__()

        base = QColor(color)
        hover_color = base.lighter(115).name()  
        pressed_color = base.darker(115).name()


        self.setFixedSize(240, 240)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};           
                border: none;
                border-radius: 28px;                 
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
        card_layout.setSpacing(10)                      
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

      
        self.image_label = QLabel()
        self.image_label.setStyleSheet("background: transparent;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(QPixmap(os.path.join(ASSETS_DIR, icon_path)).scaled(
                200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))


        self.title_label = QLabel(title_text)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"""
            color: #FFFFFF;
            font-family: '{font_family}';
            font-size: 16px;
            font-weight: bold;
            background: transparent;
        """)
        
        card_layout.addStretch()
     
        card_layout.addWidget(self.image_label)
        card_layout.addWidget(self.title_label)
        