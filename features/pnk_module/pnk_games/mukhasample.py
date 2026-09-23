import os
import math
from PySide6.QtCore import Qt, QMimeData, QSize, QPoint
from PySide6.QtGui import QDrag, QPixmap, QIcon, QPainter, QPen, QColor, QPolygon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from themes.fonts import BODY_FONT
from themes.colors import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..","..", "..", "assets", "image_content", "pnk")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class DraggableWord(QLabel):
    """A word from the word bank that the user can drag onto a blank."""

    def __init__(self, display_text: str):
        super().__init__(display_text)
        self.setStyleSheet(f"""
            font-size: 40px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            font-family: {BODY_FONT};
        """)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)

        drag.setPixmap(self.grab())
        drag.setHotSpot(event.pos())

        drag.exec(Qt.MoveAction)


class LabelDropBox(QFrame):
    """An empty box the user drags a word into. No correctness check."""
 
    def __init__(self, border_color: str =  "#3A2E1F", width=204, height=80):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedSize(width, height)
        self.setStyleSheet(f"""
            background-color: none;
            border: 4px solid {border_color} ;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.answer_label = QLabel("")
        self.answer_label.setAlignment(Qt.AlignCenter)
        self.answer_label.setStyleSheet(f"font-size: 38px; font-weight: 700; color: {CHOCO_BROWN}; border: none; font-family: {BODY_FONT}")
        layout.addWidget(self.answer_label)
 
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
 
    def dropEvent(self, event):
        self.answer_label.setText(event.mimeData().text())
        event.acceptProposedAction()


class MukhaGameSample(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(25)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(60, 50, 0, 20)
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )


        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent;")
        back_btn.clicked.connect(lambda: self.router.navigate("katawan"))
        top_bar.addWidget(back_btn)

        title = QLabel("Pagsasanay 1: Mata, Ilong, Bibig, Tainga, Buhok")
        title.setStyleSheet(f"font-size: 30px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # ---- Word bank ----
        word_bank = QFrame()
        word_bank.setMinimumWidth(800)
        word_bank.setStyleSheet(f"border: 1px solid #D9CBB0; border-radius: 4px; ")
        word_bank_row = QHBoxLayout(word_bank)
        word_bank_row.setContentsMargins(60, 20, 40, 20)
        word_bank_row.setSpacing(80)

        for word_text in ["mata", "tainga", "ilong", "bibig", "buhok", "kilay"]:
            word = DraggableWord(word_text)
            word_bank_row.addWidget(word)
        word_bank_row.addStretch()

        main_layout.addWidget(word_bank)

 
        #Diagram Layout
        diagram_layout = QHBoxLayout()
        diagram_layout.addSpacing(120)
        diagram_layout.setAlignment(Qt.AlignHCenter)
        main_layout.addLayout(diagram_layout)

        first_column = QVBoxLayout()
        first_column.addSpacing(50)
        first_column.setContentsMargins(0, 0, 100, 0)
        diagram_layout.addLayout(first_column)

        self.buhok_db = LabelDropBox(SKY_BLUE)
        first_column.addWidget(self.buhok_db)

        self.bibig_db = LabelDropBox(ELECTRIC_VIOLET)
        first_column.addWidget(self.bibig_db)

        self.ilong_db = LabelDropBox(GREEN)
        first_column.addWidget(self.ilong_db)


        self.face_image = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "mukha.png")).scaled(
            400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.face_image.setPixmap(pixmap)
        diagram_layout.addWidget(self.face_image)

        third_column = QVBoxLayout()
        third_column.addSpacing(50)
        third_column.setContentsMargins(100, 0, 0, 0)
        diagram_layout.addLayout(third_column)

        self.mata_db = LabelDropBox(CRIMSON)
        third_column.addWidget(self.mata_db)

        self.tainga_db = LabelDropBox(CHOCO_BROWN)
        third_column.addWidget(self.tainga_db)

        self.kilay_db = LabelDropBox(MEDIUM_PURPLE)
        third_column.addWidget(self.kilay_db)
      
 

 