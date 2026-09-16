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
 
    def __init__(self, width=170, height=45):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedSize(width, height)
        self.setStyleSheet(f"""
            background-color: none;
            border: 1px solid {CHOCO_BROWN} ;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.answer_label = QLabel("")
        self.answer_label.setAlignment(Qt.AlignCenter)
        self.answer_label.setStyleSheet("font-size: 20px; font-weight: 700; color: #3A2E1F; border: none;")
        layout.addWidget(self.answer_label)

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
        self.answer_label.setText(event.mimeData().text())
        self._apply_filled_style()
        event.acceptProposedAction()

class ArrowOverlay(QWidget):
    """
    A transparent widget that sits ON TOP of the diagram (image + boxes)
    and only draws the arrow lines. Since it's a separate widget placed
    LAST and raised, its paintEvent renders above everything beneath it.
    """
 
    def __init__(self, parent, arrows):
        super().__init__(parent)
        self.arrows = arrows
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)   # clicks pass through to widgets below
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#3A2E1F"), 3)
        painter.setPen(pen)
 
        for start, end in self.arrows:
            painter.drawLine(start, end)
            self._draw_arrowhead(painter, start, end)
 
    def _draw_arrowhead(self, painter: QPainter, start: QPoint, end: QPoint):
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = 12
 
        p1 = end
        p2 = QPoint(
            int(end.x() - arrow_size * math.cos(angle - math.pi / 6)),
            int(end.y() - arrow_size * math.sin(angle - math.pi / 6)),
        )
        p3 = QPoint(
            int(end.x() - arrow_size * math.cos(angle + math.pi / 6)),
            int(end.y() - arrow_size * math.sin(angle + math.pi / 6)),
        )
 
        painter.setBrush(QColor("#3A2E1F"))
        painter.drawPolygon(QPolygon([p1, p2, p3]))


class MukhaGame(QWidget):
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

        for word_text in ["mata", "tainga", "ilong", "bibig", "buhok"]:
            word = DraggableWord(word_text)
            word_bank_row.addWidget(word)
        word_bank_row.addStretch()

        main_layout.addWidget(word_bank)

      # ---- Diagram area ----
        self.diagram_area = QWidget()
        self.diagram_area.setMinimumHeight(420)
        main_layout.addWidget(self.diagram_area)
 
        # 1. Face image FIRST
        self.face_image = QLabel(self.diagram_area)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "mukha.png")).scaled(
            300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.face_image.setPixmap(pixmap)
        self.face_image.move(300, 20)
 
        # 2. Drop boxes SECOND
        self.box_hair = LabelDropBox(); self.box_hair.setParent(self.diagram_area); self.box_hair.move(30, 60)
        self.box_eyebrow = LabelDropBox(); self.box_eyebrow.setParent(self.diagram_area); self.box_eyebrow.move(650, 60)
        self.box_eye = LabelDropBox(); self.box_eye.setParent(self.diagram_area); self.box_eye.move(30, 170)
        self.box_ear = LabelDropBox(); self.box_ear.setParent(self.diagram_area); self.box_ear.move(650, 170)
        self.box_nose = LabelDropBox(); self.box_nose.setParent(self.diagram_area); self.box_nose.move(650, 260)
        self.box_mouth = LabelDropBox(); self.box_mouth.setParent(self.diagram_area); self.box_mouth.move(30, 320)
 
        # 3. Arrow overlay LAST — this is what makes arrows render on top
        self.arrows = [
            (QPoint(370, 130), QPoint(200, 90)),
            (QPoint(490, 130), QPoint(650, 90)),
            (QPoint(420, 210), QPoint(200, 200)),
            (QPoint(540, 210), QPoint(650, 200)),
            (QPoint(460, 230), QPoint(650, 290)),
            (QPoint(430, 270), QPoint(200, 350)),
        ]
        self.arrow_overlay = ArrowOverlay(self.diagram_area, self.arrows)
        self.arrow_overlay.setGeometry(0, 0, self.diagram_area.width(), self.diagram_area.height())
        self.arrow_overlay.raise_()   # ensure it's above face_image and the boxes
 
    def resizeEvent(self, event):
        # keep the overlay covering the full diagram area if the window resizes
        self.arrow_overlay.setGeometry(0, 0, self.diagram_area.width(), self.diagram_area.height())
        super().resizeEvent(event)
 