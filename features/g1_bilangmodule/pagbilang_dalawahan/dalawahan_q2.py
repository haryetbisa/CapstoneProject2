import os
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDrag, QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from themes.fonts import BODY_FONT
from themes.colors import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..","..", "..", "assets", "image_content", "salita")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class DraggableWord(QLabel):
    """A word from the word bank that the user can drag onto a blank."""

    def __init__(self, display_text: str):
        super().__init__(display_text)
        self.setStyleSheet(f"""
            font-size: 60px;
            font-weight: 700;
            color: {CHOCO_BROWN};
            font-family: {BODY_FONT};
        """)
        self.setFixedSize(100, 100)
        self.setCursor(Qt.OpenHandCursor)
        self.setAlignment(Qt.AlignCenter)
  

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


class BlankDropTarget(QLabel):
    """
    An underlined blank inside the sentence. Starts empty (just a line),
    and shows whatever word gets dropped on it — no correctness check.
    """

    def __init__(self, min_width: int = 180):
        super().__init__("")
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(min_width)
        self.setFixedHeight(90)
        self._apply_empty_style()

    def _apply_empty_style(self):
        self.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            border: none;
            border-bottom: 4px solid {CHOCO_BROWN};
        """)

    def _apply_filled_style(self):
        self.setStyleSheet(f"""
            font-size: 80px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            border: none;
            border-bottom: 4px solid {CHOCO_BROWN};
            background-color: {BRIGHT_YELLOW};
            font-family: {BODY_FONT};
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        dropped_text = event.mimeData().text()
        self.setText(dropped_text)
        self._apply_filled_style()
        event.acceptProposedAction()


class BilangLvl6(QWidget):
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
        back_btn.clicked.connect(lambda: self.router.navigate("bilang_g1"))
        top_bar.addWidget(back_btn)

        title = QLabel("Pagsasanay 6: Dalawahang Pagbilang")
        title.setStyleSheet(f"font-size: 30px; font-weight: 600; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Numbers Bank
        word_bank = QFrame()
        word_bank.setMinimumWidth(300)
        word_bank.setStyleSheet(f"border: 1px solid #D9CBB0; border-radius: 4px; ")

    
        word_bank_row = QHBoxLayout(word_bank)
        word_bank_row.setContentsMargins(20, 20, 20, 20)
        word_bank_row.setSpacing(60)
        word_bank_row.setAlignment(Qt.AlignCenter)

        word_bank_row.addStretch(1)

        for word_text in ["30", "26", "32", "38", "40", "42"]:
            word = DraggableWord(word_text)
            word_bank_row.addWidget(word)

        word_bank_row.addStretch(1)

        main_layout.addWidget(word_bank)


        # Image & sentence words at blank
        sentence_layout = QVBoxLayout()
        sentence_layout.setSpacing(40)
        sentence_layout.setAlignment(Qt.AlignCenter)

        # First Line
        first_line = QHBoxLayout()
        first_line.setSpacing(80)
        first_line.setAlignment(Qt.AlignCenter)
        sentence_layout.addLayout(first_line)

        self.blank1 = BlankDropTarget(min_width=100)
        first_line.addWidget(self.blank1)

        first_num = QLabel("28")
        first_num.setStyleSheet(f"font-size: 90px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        first_line.addWidget(first_num)

        self.blank2 = BlankDropTarget(min_width=100)
        first_line.addWidget(self.blank2)

        self.blank3 = BlankDropTarget(min_width=100)
        first_line.addWidget(self.blank3)


        # Second Line
        second_line = QHBoxLayout()
        second_line.setSpacing(80)
        second_line.setAlignment(Qt.AlignCenter)
        sentence_layout.addLayout(second_line)

        second_num = QLabel("34")
        second_num.setStyleSheet(f"font-size: 90px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        second_line.addWidget(second_num)

        third_num = QLabel("36")
        third_num.setStyleSheet(f"font-size: 90px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        second_line.addWidget(third_num)

        self.blank4 = BlankDropTarget(min_width=100)
        second_line.addWidget(self.blank4)

        self.blank5 = BlankDropTarget(min_width=100)
        second_line.addWidget(self.blank5)


        main_layout.addLayout(sentence_layout)
        main_layout.addStretch()