# para sa dashboard buttons na may png at words
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QPixmap, QColor
from themes.colors import *
from assets.image import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "assets", "image"))

class CardsButton(QPushButton):
    def __init__(self, title_text, icon_path = "giraffe.png", color = "gray", font_family= "Poppins", parent = None):
        super().__init__()

        base = QColor(color)
        hover_color = base.lighter(115).name()  
        pressed_color = base.darker(115).name()


        self.setFixedSize(260, 260)
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
                160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))


        self.title_label = QLabel(title_text)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"""
            color: #FFFFFF;
            font-family: '{font_family}';
            font-size: 22px;
            font-weight: bold;
            background: transparent;
        """)
        
        card_layout.addStretch()
     
        card_layout.addWidget(self.image_label)
        card_layout.addWidget(self.title_label)

        self.prog_bar = QProgressBar()
        self.prog_bar.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.prog_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prog_bar.setRange(0, 100)
        self.prog_bar.setValue(0)  # Default start at 0%
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
        
        card_layout.addWidget(self.prog_bar)

    def set_progress(self, percent: int):
        """Dynamically updates the progress bar value and text label (0% - 100%)."""
        clamped_val = max(0, min(100, percent))
        self.prog_bar.setValue(clamped_val)