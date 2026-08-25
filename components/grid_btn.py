#para sa grid layout na content na may letters/numbers

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QColor
from themes.colors import *
from themes.fonts import BODY_FONT


class GridButton(QPushButton):
    def __init__(self, title_text, color = "gray", font_family= "noot", parent = None):
        super().__init__()

        self.clicked.connect(lambda: print("GridButton itself was clicked!"))

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
        self.aralin.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.aralin.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.aralin.setStyleSheet(f"""
            color: {WHITE};
            font-family: {BODY_FONT};
            font-size: 16px;
            font-weight: 500;
            background: transparent;
        """)


        self.title_label = QLabel(title_text)
        self.title_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"""
            color: #FFFFFF;
            font-family: '{font_family}';
            font-size: 100px;
            font-weight: 800;
            background: transparent;
        """)

        self.prog_bar = QProgressBar()
        self.prog_bar.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.prog_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prog_bar.setRange(0, 100)
        self.prog_bar.setValue(30)
        self.prog_bar.setFixedHeight(18)
        self.prog_bar.setTextVisible(True)  

        self.prog_bar.setStyleSheet(f"""
            QProgressBar {{
                height: 18px;
                width: 14px;
                border-radius: 9px;
                font-size: 12px;
                font-weight: 600;
                font-family: {BODY_FONT};
                text-align: center;
                color: {HONEY_YELLOW};
            }}
            QProgressBar::chunk {{
                background-color: {YELLOW};
                border-radius: 9px;
            }}
        """)
        
        card_layout.addWidget(self.aralin)
        card_layout.addWidget(self.title_label)
        card_layout.addWidget(self.prog_bar)
       
        