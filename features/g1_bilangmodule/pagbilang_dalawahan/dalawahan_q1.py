import os
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDrag, QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from themes.fonts import BODY_FONT
from themes.colors import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..","..", "..", "assets", "image_content", "bilang_g1")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class DraggableWord(QLabel):
    """A pic from the picture bank that the user can drag onto a blank."""

    def __init__(self, word_id: str, image_path: str, size: int = 200):
        super().__init__()
        self.word_id = word_id
        self.image_path = image_path

        pixmap = QPixmap(image_path).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(200, 200)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.word_id)
        mime_data.setProperty("image_path", self.image_path)

        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos())

        drag.exec(Qt.MoveAction)


class BlankDropTarget(QLabel):
    """
    An underlined blank inside the sentence.
    """

    def __init__(self, size: int = 250):
        super().__init__("")
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.target_size = size
        self._apply_empty_style()

        self.setFixedSize(size, size)
        self._apply_empty_style()

    def _apply_empty_style(self):
        self.setStyleSheet(f"""
            border: 2px dashed {CHOCO_BROWN};
            border-radius: 10px;
            background-color: none;
        """)

    def _apply_filled_style(self):
        self.setStyleSheet(f"""
            border: 2px solid {CHOCO_BROWN};
            border-radius: 10px;
            background-color: {PASTEL_YELLOW};
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        image_path = event.mimeData().property("image_path")
        
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                self.target_size - 10, 
                self.target_size - 10, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.setPixmap(pixmap)
            self._apply_filled_style()
            event.acceptProposedAction()


class BilangLvl5(QWidget):
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

        title = QLabel("Pagsasanay 5: Dalawahang Pagbilang")
        title.setStyleSheet(f"font-size: 30px; font-weight: 600; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        #Picture Bank
        pic_bank = QFrame()
        pic_bank.setMinimumWidth(800)
        pic_bank.setStyleSheet(f"border: 1px solid #D9CBB0; border-radius: 4px; ")

        pic_bank_row = QHBoxLayout(pic_bank)
        pic_bank_row.setContentsMargins(20, 20, 20, 20)
        pic_bank_row.setSpacing(40)

        pic_bank_row.addStretch(1)

        for word_id, image_file in [
                ("apat", "4pencil.png"),
                ("anim", "6pencil.png"),
                ("sampu", "10pencil.png")
            ]:
            word = DraggableWord(word_id, os.path.join(IMAGE_DIR, image_file))
            pic_bank_row.addWidget(word)

        pic_bank_row.addStretch(1)

        main_layout.addWidget(pic_bank)


        # Image & sentence words at blank
        image_layout = QHBoxLayout()
        image_layout.setSpacing(10)


        dalawa = QLabel()
        dalawa.setAlignment(Qt.AlignCenter)
        dalawa.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "2pencil.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image_layout.addWidget(dalawa)

        self.blank1 = BlankDropTarget(size=200)
        image_layout.addWidget(self.blank1)

        self.blank2 = BlankDropTarget(size=200)
        image_layout.addWidget(self.blank2)

        walo = QLabel()
        walo.setAlignment(Qt.AlignCenter)
        walo.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "8pencil.png")).scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image_layout.addWidget(walo)

        self.blank3 = BlankDropTarget(size=200)
        image_layout.addWidget(self.blank3)


        main_layout.addLayout(image_layout)
        main_layout.addStretch()