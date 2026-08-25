from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from themes.fonts import BODY_FONT
from themes.colors import *


class ChoicesButton(QPushButton):
    def __init__(self, title_text, color = "gray", parent = None):
        super().__init__()

        base = QColor(color)
        hover_color = base.lighter(115).name()  
        pressed_color = base.darker(115).name()


        self.setFixedSize(300, 150)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};           
                border: none;
                border-radius: 14px;                 
            }}
            QPushButton:hover {{
                background-color: {hover_color};         
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};         
            }}
        """)

        btn_layout = QVBoxLayout(self)
        btn_layout.setContentsMargins(15, 25, 15, 20)  
        btn_layout.setSpacing(40)                      
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        self.aralin = QLabel("Aralin:")
        self.aralin.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.aralin.setStyleSheet(f"""
            color: {WHITE};
            font-family: {BODY_FONT};
            font-size: 16px;
            font-weight: 500;
            background: transparent;
        """)


        self.title_label = QLabel(title_text)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"""
            color: {WHITE};
            font-family: {BODY_FONT};
            font-size: 58px;
            font-weight: 800;
            background: transparent;
        """)
        btn_layout.addWidget(self.title_label)







