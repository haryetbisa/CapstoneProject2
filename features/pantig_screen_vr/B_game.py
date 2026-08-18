import os
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "pantig")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "icons")

class Dot(QLabel):
    """A small circular anchor point. Left dots are draggable; right dots are drop targets."""

    def __init__(self, dot_id: str, is_source: bool, parent_game):
        super().__init__()
        self.dot_id = dot_id
        self.is_source = is_source
        self.game = parent_game

        self.setFixedSize(20, 20)
        self.setStyleSheet("background-color: #3A2E1F; border-radius: 10px;")
        if is_source:
            self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if not self.is_source or event.button() != Qt.LeftButton:
            return
        self.grabMouse()
        self.game.start_drag(self)

    def mouseMoveEvent(self, event):
        if not self.is_source:
            return
        global_pos = self.mapToGlobal(event.pos())
        game_pos = self.game.mapFromGlobal(global_pos)
        self.game.update_temp_line(game_pos)

    def mouseReleaseEvent(self, event):
        if not self.is_source:
            return
        self.releaseMouse()

        global_pos = self.mapToGlobal(event.pos())
        target_widget = QApplication.widgetAt(global_pos)

        if isinstance(target_widget, Dot) and not target_widget.is_source:
            self.game.finalize_connection(self, target_widget)
        else:
            self.game.cancel_drag()


class MatchingBa(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.connections = []   # list of (source_dot, target_dot) — no correctness tracked
        self.dragging_from = None
        self.temp_end_point = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)

        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_bar)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("pantig"))

   
        pagsasanay = QLabel("Pagsasanay")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: {CHOCO_BROWN};               
        """)


        top_bar.addWidget(back_btn)
        top_bar.addWidget(pagsasanay)
        top_bar.setSpacing(20)

        rows_layout = QVBoxLayout()
        rows_layout.setSpacing(40)
        rows_layout.setContentsMargins(80, 60, 80, 30)
        main_layout.addLayout(rows_layout)

        items = [
            ("house", "bahay.png", "bahay", "Ba - hay"),
            ("glass", "Baso.png", "bata", "Ba - ta"),
            ("kid", "bata.png", "baso", "Ba - so"),
        ]

        for image_id, image_file, word_id, word_display in items:
            row = QHBoxLayout()

            image_label = QLabel()
            image_label.setPixmap(
                QPixmap(os.path.join(IMAGE_DIR, image_file)).scaled(
                    160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
            row.addWidget(image_label)

            source_dot = Dot(image_id, is_source=True, parent_game=self)
            row.addWidget(source_dot)

            row.addStretch()

            target_dot = Dot(word_id, is_source=False, parent_game=self)
            row.addWidget(target_dot)

            word_label = QLabel(word_display)
            word_label.setStyleSheet(f"font-size: 46px; font-family:{BODY_FONT}; font-weight: 800; color: #3A2E1F;")
            row.addWidget(word_label)

            rows_layout.addLayout(row)


        main_layout.addStretch()

    def start_drag(self, source_dot: Dot):
        self.dragging_from = source_dot
        self.temp_end_point = self.dot_center(source_dot)
        self.update()

    def update_temp_line(self, pos: QPoint):
        self.temp_end_point = pos
        self.update()

    def cancel_drag(self):
        self.dragging_from = None
        self.temp_end_point = None
        self.update()

    def finalize_connection(self, source_dot: Dot, target_dot: Dot):
        # replace any previous line from this same source
        self.connections = [c for c in self.connections if c[0] != source_dot]
        self.connections.append((source_dot, target_dot))

        self.dragging_from = None
        self.temp_end_point = None
        self.update()

    def dot_center(self, dot: Dot) -> QPoint:
        return dot.mapTo(self, dot.rect().center())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(f"{CADET_BLUE}"), 8)
        painter.setPen(pen)

        # finalized lines
        for source_dot, target_dot in self.connections:
            painter.drawLine(self.dot_center(source_dot), self.dot_center(target_dot))

        # line currently being dragged
        if self.dragging_from and self.temp_end_point:
            painter.drawLine(self.dot_center(self.dragging_from), self.temp_end_point)