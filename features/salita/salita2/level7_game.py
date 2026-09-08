import os
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "salita")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class Dot(QLabel):
    """A small circular anchor point. Left dots are draggable; right dots are drop targets."""

    def __init__(self, is_source: bool, parent_game):
        super().__init__()
        self.is_source = is_source
        self.game = parent_game

        self.setFixedSize(20, 20)
        self.setStyleSheet(f"background-color: {CHOCO_BROWN}; border-radius: 20px;")
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


class Salita7Game(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.connections = []   # list of (source_dot, target_dot) — no correctness tracked
        self.dragging_from = None
        self.temp_end_point = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)

        # Top bar
        top_bar = QHBoxLayout()
        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(30, 30))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent;")
        back_btn.clicked.connect(lambda: self.router.navigate("salita"))
        top_bar.addWidget(back_btn)

        title = QLabel("Pagsasanay 7: Salitang Magkatugma")
        title.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT} ;")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Rows of matching items — same image+word appears on both sides
        rows_layout = QVBoxLayout()
        rows_layout.setSpacing(40)
        rows_layout.setContentsMargins(60, 40, 60, 20)
        main_layout.addLayout(rows_layout)

        # each row: (left_image, left_word, right_image, right_word) — can be fully different per side
        items = [
            ("aso.png", "aso", "pusa.png", "kuting"),
            ("gunting.png", "gunting", "araw.png", "araw"),
            ("gatas.png", "gatas", "baso.png", "baso"),
            ("pagong.png", "pagong", "prutas.png", "prutas"),
            ("ilaw.png", "ilaw", "gulong.png", "gulong"),
        ]

        for left_image_file, left_word_text, right_image_file, right_word_text in items:
            row = QHBoxLayout()

            # ---- LEFT: image + word ----
            left_image = QLabel()
            left_path = os.path.join(IMAGE_DIR, left_image_file)
            if os.path.exists(left_path):
                left_image.setPixmap(
                    QPixmap(left_path).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            row.addWidget(left_image)

            left_word = QLabel(left_word_text)
            left_word.setStyleSheet(f"font-size: 30px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
            row.addWidget(left_word)

            source_dot = Dot(is_source=True, parent_game=self)
            row.addWidget(source_dot)

            row.addStretch()

            # ---- RIGHT: dot + image + word ----
            target_dot = Dot(is_source=False, parent_game=self)
            row.addWidget(target_dot)

            right_image = QLabel()
            right_path = os.path.join(IMAGE_DIR, right_image_file)
            if os.path.exists(right_path):
                right_image.setPixmap(
                    QPixmap(right_path).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            row.addWidget(right_image)

            right_word = QLabel(right_word_text)
            right_word.setStyleSheet(f"font-size: 30px; font-weight: 700; color:{CHOCO_BROWN}; font-family: {BODY_FONT} ;")
            row.addWidget(right_word)

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

        pen = QPen(QColor(MAGENTA), 6)
        painter.setPen(pen)

        for source_dot, target_dot in self.connections:
            painter.drawLine(self.dot_center(source_dot), self.dot_center(target_dot))

        if self.dragging_from and self.temp_end_point:
            painter.drawLine(self.dot_center(self.dragging_from), self.temp_end_point)