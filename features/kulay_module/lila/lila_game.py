import os
from PySide6.QtCore import QMimeData, QSize, Qt, QUrl
from PySide6.QtGui import QColor, QDrag, QIcon, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(
    BASE_DIR, "..", "..", "..", "assets", "image_content", "kulay"
)
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
SOUNDS_DIR = os.path.join(
    BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong"
)


class DraggableIcon(QLabel):
    """An image the user can pick up and drag anywhere."""

    def __init__(self, image_path: str, filename: str, size: int = 160):
        super().__init__()
        self.image_path = image_path
        self.filename = filename

        pixmap = QPixmap(image_path)
        self.setPixmap(
            pixmap.scaled(
                size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.filename)
        drag.setMimeData(mime_data)

        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos())

        self.hide()
        result = drag.exec(Qt.MoveAction)
        if result != Qt.MoveAction:
            self.show()


class DropBox(QLabel):
    """The box — accepts dropped items, provides border glow feedback, and delegates evaluation."""

    def __init__(self, image_path: str, parent_game=None, size=(300, 300)):
        super().__init__()
        self.parent_game = parent_game
        self.setAcceptDrops(True)
        self.setFixedSize(*size)
        self.setAlignment(Qt.AlignCenter)

        # Base styling setup
        self.default_style = """
            QLabel {
                border: 3px dashed #B8860B;
                border-radius: 20px;
                background-color: transparent;
            }
        """
        self.correct_style = """
            QLabel {
                border: 5px solid #2E7D32;
                border-radius: 20px;
                background-color: rgba(76, 175, 80, 0.15);
            }
        """
        self.wrong_style = """
            QLabel {
                border: 5px solid #C62828;
                border-radius: 20px;
                background-color: rgba(244, 67, 54, 0.15);
            }
        """

        self.setStyleSheet(self.default_style)

        box_pixmap = QPixmap(image_path)
        self.setPixmap(
            box_pixmap.scaled(
                *size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            filename = event.mimeData().text()

            # Change border highlights on hover
            if (
                self.parent_game
                and hasattr(self.parent_game, "correct_items")
                and filename in self.parent_game.correct_items
            ):
                self.setStyleSheet(self.correct_style)
            else:
                self.setStyleSheet(self.wrong_style)

    def dragLeaveEvent(self, event):
        """Restores default border when item leaves."""
        self.setStyleSheet(self.default_style)
        event.accept()

    def dropEvent(self, event):
        """Restores default border and processes dropped item."""
        self.setStyleSheet(self.default_style)
        filename = event.mimeData().text()
        source_widget = event.source()

        if self.parent_game and hasattr(self.parent_game, "handle_item_drop"):
            self.parent_game.handle_item_drop(source_widget, filename)

        event.acceptProposedAction()


class DragDropPurple(QWidget):

    def __init__(self, router):
        super().__init__()
        self.router = router

        # Validation rules
        self.correct_items = ["grapes.png", "purple_umbrella.png"]
        self.REQUIRED_CORRECT_COUNT = 2
        self.current_correct_count = 0

        # Audio setup
        self.audio_output = QAudioOutput(self)
        self.audio_player = QMediaPlayer(self)
        self.audio_player.setAudioOutput(self.audio_output)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(100, 50, 0, 20)
        top_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter
        )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(
            "border: none; background-color: none; border-radius: 6px"
        )
        back_btn.clicked.connect(lambda: self.router.navigate("lila"))

        pagsasanay = QLabel("Aralin: Lila")
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

        # Draggable items container
        self.items_row = QHBoxLayout()
        self.items_row.setSpacing(100)
        self.items_row.setContentsMargins(0, 0, 0, 40)
        self.items_row.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(self.items_row)

        # Drop target box
        self.drop_box = DropBox(
            os.path.join(IMAGE_DIR, "purple_box.png"), parent_game=self
        )
        main_layout.addWidget(self.drop_box, alignment=Qt.AlignCenter)

        # Feedback text
        self.feedback_label = QLabel("", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet(f"""
            font-size: 24px;
            font-family: {BODY_FONT};
            font-weight: bold;
            color: {CHOCO_BROWN};
            margin-top: 20px;
        """)
        main_layout.addWidget(self.feedback_label)

        self.item_images = [
            "whale.png",
            "grapes.png",
            "bat.png",
            "purple_umbrella.png",
        ]
        self.active_icons = []
        self.setup_items()

    def setup_items(self):
        """Resets and creates draggable icon instances."""
        for icon in self.active_icons:
            icon.setParent(None)
            icon.deleteLater()
        self.active_icons.clear()

        for filename in self.item_images:
            icon = DraggableIcon(
                os.path.join(IMAGE_DIR, filename), filename=filename
            )
            self.items_row.addWidget(icon)
            self.active_icons.append(icon)

    def play_sound(self, filename: str):
        """Plays audio feedback."""
        sound_path = os.path.join(SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            abs_path = os.path.abspath(sound_path)
            self.audio_player.setSource(QUrl.fromLocalFile(abs_path))
            self.audio_player.play()

    def handle_item_drop(self, source_widget: DraggableIcon, filename: str):
        """Evaluates correctness when an item is dropped into the box."""
        if filename in self.correct_items:
            self.current_correct_count += 1
            source_widget.deleteLater()
            if source_widget in self.active_icons:
                self.active_icons.remove(source_widget)

            if self.current_correct_count >= self.REQUIRED_CORRECT_COUNT:
                self.feedback_label.setText("✅ MAGALING! TAMA LAHAT!")
                self.feedback_label.setStyleSheet(
                    f"font-size: 26px; color: green; font-family: {BODY_FONT};"
                    " font-weight: bold;"
                )
                self.play_sound("correct.wav")
            else:
                self.feedback_label.setText("Tama! Isa pa!")
                self.feedback_label.setStyleSheet(
                    f"font-size: 24px; color: green; font-family: {BODY_FONT};"
                    " font-weight: bold;"
                )
        else:
            # Wrong color penalty: Play wrong sound and reset
            self.play_sound("wrong.wav")
            self.feedback_label.setText(
                "❌ SUBUKAN ULIT! Maling kulay! Na-reset ang laro."
            )
            self.feedback_label.setStyleSheet(
                f"font-size: 24px; color: red; font-family: {BODY_FONT};"
                " font-weight: bold;"
            )
            self.reset_game()

    def reset_game(self):
        """Resets target score and restores item layout."""
        self.current_correct_count = 0
        self.setup_items()