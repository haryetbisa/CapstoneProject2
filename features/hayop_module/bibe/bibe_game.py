import os
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDrag, QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "hayop")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")

class DraggableAnimal(QLabel):
    """The dog — the thing being dragged."""

    def __init__(self, image_path: str, size: int = 200):
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
        mime_data.setText("dragged")   
        drag.setMimeData(mime_data)

        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos())

        drag.exec(Qt.MoveAction)


class HabitatTarget(QLabel):
    """A possible drop destination — accepts any drop, no validation."""

    def __init__(self, image_path: str, size: int = 220):
        super().__init__()
        self.setAcceptDrops(True)   

        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAlignment(Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        print("Dropped here!")
        event.acceptProposedAction()


class BibeGame(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(40)

        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_bar)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("bibevs"))

   
        pagsasanay = QLabel("Pagsasanay: Bibe")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)


        top_bar.addWidget(back_btn)
        top_bar.addWidget(pagsasanay)
        top_bar.setSpacing(20)

       
        habitats_row = QHBoxLayout()
        habitats_row.setSpacing(120)
        habitats_row.setContentsMargins(0, 40, 0, 40)
        habitats_row.setAlignment(Qt.AlignCenter)

        forest = HabitatTarget(os.path.join(IMAGE_DIR, "forest.png"))
        rabbit_hole = HabitatTarget(os.path.join(IMAGE_DIR, "rabbit_hole.png"))
        duck_pond = HabitatTarget(os.path.join(IMAGE_DIR, "duck_pond.png"))

        habitats_row.addWidget(forest)
        habitats_row.addWidget(rabbit_hole)
        habitats_row.addWidget(duck_pond)
        main_layout.addLayout(habitats_row)

    
        shelter_row = QHBoxLayout()
        shelter_row.setAlignment(Qt.AlignCenter)
        shelter_row.setContentsMargins(0, 40, 0, 0)

        animal = DraggableAnimal(os.path.join(IMAGE_DIR, "bibe.png"))
        shelter_row.addWidget(animal)
        main_layout.addLayout(shelter_row)

        main_layout.addStretch()