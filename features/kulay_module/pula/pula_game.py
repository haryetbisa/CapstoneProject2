import os
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDrag, QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "kulay")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class DraggableIcon(QLabel):
    """An image the user can pick up and drag anywhere."""

    def __init__(self, image_path: str, size: int = 160):
        super().__init__()
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText("dragged")   # no meaning needed yet, just required for the drag to work
        drag.setMimeData(mime_data)

        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos())

        drag.exec(Qt.MoveAction)


class DropBox(QLabel):
    """The box — accepts ANY dropped item, no validation."""

    def __init__(self, image_path: str, size=(240, 190)):
        super().__init__()
        self.setAcceptDrops(True)   # required, or drops are ignored entirely
        self.setFixedSize(*size)
        self.setAlignment(Qt.AlignCenter)

        box_pixmap = QPixmap(image_path)
        self.setPixmap(box_pixmap.scaled(*size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        print("Something was dropped in the box!")
        event.acceptProposedAction()


class DragDropDemoScreenRed(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 20, 0, 60)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("kulay"))

   
        pagsasanay = QLabel("Aralin: Pula")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        
        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(50)
        main_layout.addLayout(top_layout)

        # Row of draggable items
        items_row = QHBoxLayout()
        items_row.setSpacing(60)
        items_row.setAlignment(Qt.AlignCenter)

        item_images = ["apple.png", "strawberry.png", "blue_popsicle.png", "turtle.png"]
        for filename in item_images:
            icon = DraggableIcon(os.path.join(IMAGE_DIR, filename))
            items_row.addWidget(icon)

        main_layout.addLayout(items_row)

        # The box
        drop_box = DropBox(os.path.join(IMAGE_DIR, "red_box.png"))
        main_layout.addWidget(drop_box, alignment=Qt.AlignCenter)