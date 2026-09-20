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
        self.setFixedHeight(50)
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
            font-size: 40px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            border: none;
            border-bottom: 4px solid {CHOCO_BROWN};
            background-color: {PASTEL_YELLOW};
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


class Salita11Game(QWidget):
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
        back_btn.clicked.connect(lambda: self.router.navigate("salita"))
        top_bar.addWidget(back_btn)

        title = QLabel("Pagsasanay 11: Pangungusap")
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
        word_bank_row.setSpacing(50)

        for word_text in ["pusa", "natutulog", "tumatakbo", "daga", "nasayaw"]:
            word = DraggableWord(word_text)
            word_bank_row.addWidget(word)
        word_bank_row.addStretch()

        main_layout.addWidget(word_bank)

        # Image & sentence words at blank
        sentence_layout = QVBoxLayout()
        sentence_layout.setSpacing(10)

        picture_label = QLabel()
        picture_label.setAlignment(Qt.AlignCenter)
        picture_label.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "halimbawa.png")).scaled(
                300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        sentence_layout.addWidget(picture_label)

        # Line 1: "Ang ____ ay"
        line1 = QHBoxLayout()
        line1.setAlignment(Qt.AlignCenter)
        line1.setSpacing(10)

        ang_label = QLabel("Ang")
        ang_label.setStyleSheet(f"font-size: 40px; font-weight: 800; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        line1.addWidget(ang_label)

        self.blank1 = BlankDropTarget(min_width=200)
        line1.addWidget(self.blank1)

        ay_label = QLabel("ay")
        ay_label.setStyleSheet(f"font-size: 40px; font-weight: 800; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        line1.addWidget(ay_label)

        self.blank2 = BlankDropTarget(min_width=200)
        line1.addWidget(self.blank2)
        
        period_label = QLabel(".")
        period_label.setStyleSheet(f"font-size: 40px; font-weight: 800; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        line1.addWidget(period_label)

        sentence_layout.addLayout(line1)

        # Line 2: "____ ."
        line2 = QHBoxLayout()
        line2.setSpacing(15)

        self.blank2 = BlankDropTarget(min_width=300)
        line2.addWidget(self.blank2)


        main_layout.addLayout(sentence_layout)
        main_layout.addStretch()