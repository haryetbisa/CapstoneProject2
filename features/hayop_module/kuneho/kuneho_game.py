import os
from PySide6.QtCore import QMimeData, QPoint, QSize, Qt, QUrl
from PySide6.QtGui import QDrag, QIcon, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
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
    BASE_DIR, "..", "..", "..", "assets", "image_content", "hayop"
)
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
SOUNDS_DIR = os.path.join(
    BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong"
)


class DraggableAnimal(QLabel):
    def __init__(self, image_path: str, animal_id: str, size: int = 200):
        super().__init__()
        self.image_path = image_path
        self.animal_id = animal_id
        self.drag_start_position = QPoint()

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.setPixmap(
                pixmap.scaled(
                    size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton) or not self.isVisible():
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.animal_id)
        drag.setMimeData(mime_data)

        if self.pixmap():
            drag.setPixmap(self.pixmap())
            drag.setHotSpot(event.pos())

        self.setCursor(Qt.ClosedHandCursor)
        self.hide()
        result = drag.exec(Qt.CopyAction | Qt.MoveAction)
        if result != Qt.MoveAction and result != Qt.CopyAction:
            self.show()
        self.setCursor(Qt.OpenHandCursor)


class HabitatTarget(QLabel):
    def __init__(
        self,
        image_path: str,
        habitat_id: str,
        parent_game=None,
        size=(220, 220),
    ):
        super().__init__()
        self.habitat_id = habitat_id
        self.parent_game = parent_game
        self.setAcceptDrops(True)
        self.setFixedSize(*size)
        self.setAlignment(Qt.AlignCenter)

        self.default_style = """
            QLabel {
                border: 3px dashed #8D6E63;
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
        if not box_pixmap.isNull():
            self.setPixmap(
                box_pixmap.scaled(
                    *size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

            if (
                self.parent_game
                and hasattr(self.parent_game, "target_habitat_id")
                and self.habitat_id in self.parent_game.target_habitat_id
            ):
                self.setStyleSheet(self.correct_style)
            else:
                self.setStyleSheet(self.wrong_style)

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        event.accept()

    def dropEvent(self, event):
        self.setStyleSheet(self.default_style)
        animal_id = event.mimeData().text()
        source_widget = event.source()

        if self.parent_game and hasattr(self.parent_game, "handle_item_drop"):
            self.parent_game.handle_item_drop(
                source_widget, animal_id, self.habitat_id
            )

        event.acceptProposedAction()


class KunehoGame(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.animal_id = "kuneho"
        self.target_habitat_id = "rabbit_hole"

        self.audio_output = QAudioOutput(self)
        self.audio_player = QMediaPlayer(self)
        self.audio_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.8)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(60, 50, 0, 20)
        top_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter
        )

        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(
            "border: none; background-color: transparent; border-radius: 6px;"
        )
        back_btn.clicked.connect(self.handle_back)

        pagsasanay = QLabel("Pagsasanay: Kuneho")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};             
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(20)
        main_layout.addLayout(top_layout)

        habitats_row = QHBoxLayout()
        habitats_row.setSpacing(80)
        habitats_row.setContentsMargins(0, 20, 0, 20)
        habitats_row.setAlignment(Qt.AlignCenter)

        self.frog_pond = HabitatTarget(
            os.path.join(IMAGE_DIR, "frog_pond.png"),
            habitat_id="frog_pond",
            parent_game=self,
        )
        self.rabbit_hole = HabitatTarget(
            os.path.join(IMAGE_DIR, "rabbit_hole.png"),
            habitat_id="rabbit_hole",
            parent_game=self,
        )
        self.chicken_house = HabitatTarget(
            os.path.join(IMAGE_DIR, "chicken_house.png"),
            habitat_id="chicken_house",
            parent_game=self,
        )

        habitats_row.addWidget(self.frog_pond)
        habitats_row.addWidget(self.rabbit_hole)
        habitats_row.addWidget(self.chicken_house)
        main_layout.addLayout(habitats_row)

        self.animal_row = QHBoxLayout()
        self.animal_row.setAlignment(Qt.AlignCenter)
        self.animal_row.setContentsMargins(0, 20, 0, 10)
        main_layout.addLayout(self.animal_row)

        self.feedback_label = QLabel("", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet(f"""
            font-size: 24px;
            font-family: {BODY_FONT};
            font-weight: bold;
            color: {CHOCO_BROWN};
            margin-top: 10px;
        """)
        main_layout.addWidget(self.feedback_label)

        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.setSpacing(20)

        self.restart_btn = QPushButton(" Restart")
        restart_icon_path = os.path.join(ICONS_DIR, "reset_icon.png")
        if os.path.exists(restart_icon_path):
            self.restart_btn.setIcon(QIcon(restart_icon_path))
        self.restart_btn.setCursor(Qt.PointingHandCursor)
        self.restart_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MARIGOLD};
                color: white;
                font-family: {BODY_FONT};
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 24px;
            }}
            QPushButton:hover {{
                background-color: #E08E00;
            }}
        """)
        self.restart_btn.hide()
        self.restart_btn.clicked.connect(self.reset_game)

        self.next_btn = QPushButton("Susunod ➔")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2E7D32;
                color: white;
                font-family: {BODY_FONT};
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 24px;
            }}
            QPushButton:hover {{
                background-color: #1B5E20;
            }}
        """)
        self.next_btn.hide()
        self.next_btn.clicked.connect(self.handle_next)

        action_layout.addWidget(self.restart_btn)
        action_layout.addWidget(self.next_btn)
        main_layout.addLayout(action_layout)

        self.active_animal = None
        self.setup_items()

        main_layout.addStretch()

    def setup_items(self):
        if self.active_animal:
            self.active_animal.setParent(None)
            self.active_animal.deleteLater()
            self.active_animal = None

        self.active_animal = DraggableAnimal(
            os.path.join(IMAGE_DIR, "kuneho.png"), animal_id=self.animal_id
        )
        self.animal_row.addWidget(self.active_animal)

    def play_sound(self, filename: str):
        sound_path = os.path.join(SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            abs_path = os.path.abspath(sound_path)
            self.audio_player.setSource(QUrl.fromLocalFile(abs_path))
            self.audio_player.play()

    def handle_item_drop(
        self,
        source_widget: DraggableAnimal,
        animal_id: str,
        target_habitat_id: str,
    ):
        if target_habitat_id in self.target_habitat_id:
            if source_widget:
                source_widget.deleteLater()
                self.active_animal = None

            self.feedback_label.setText("✅ MAGALING! TAMA ANG TAHANAN NG KUNEHO!")
            self.feedback_label.setStyleSheet(
                f"font-size: 26px; color: green; font-family: {BODY_FONT}; font-weight: bold;"
            )
            self.play_sound("correct.wav")
            self.restart_btn.show()
            self.next_btn.show()
        else:
            self.play_sound("wrong.wav")
            self.feedback_label.setText(
                "❌ SUBUKAN ULIT! Hindi 'yan ang bahay ng kuneho."
            )
            self.feedback_label.setStyleSheet(
                f"font-size: 24px; color: red; font-family: {BODY_FONT}; font-weight: bold;"
            )
            self.reset_game()

    def reset_game(self):
        self.restart_btn.hide()
        self.next_btn.hide()
        self.setup_items()

    def showEvent(self, event):
        self.reset_game()
        self.feedback_label.setText("")
        super().showEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("kuneho_lesson")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("manok_lesson")