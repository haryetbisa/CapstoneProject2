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
from session import AppSession
from Database.queries import log_activity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(
    BASE_DIR, "..", "..", "..", "assets", "image_content", "kulay"
)
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
SOUNDS_DIR = os.path.join(
    BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong"
)
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "VS Kulay")
INSTRUCTION_SOUND_FILE = "Kulay Instruction.mp3" 


class DraggableIcon(QLabel):
    def __init__(self, image_path: str, filename: str, size: int = 160):
        super().__init__()
        self.image_path = image_path
        self.filename = filename
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
        mime_data.setText(self.filename)
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


class DropBox(QLabel):
    def __init__(self, image_path: str, parent_game=None, size=(300, 300)):
        super().__init__()
        self.parent_game = parent_game
        self.setAcceptDrops(True)
        self.setFixedSize(*size)
        self.setAlignment(Qt.AlignCenter)

        self.default_style = """
            QLabel {
                border: 3px dashed #5D4037;
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
            filename = event.mimeData().text()

            if (
                self.parent_game
                and hasattr(self.parent_game, "correct_items")
                and filename in self.parent_game.correct_items
            ):
                self.setStyleSheet(self.correct_style)
            else:
                self.setStyleSheet(self.wrong_style)

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        event.accept()

    def dropEvent(self, event):
        self.setStyleSheet(self.default_style)
        filename = event.mimeData().text()
        source_widget = event.source()

        if self.parent_game and hasattr(self.parent_game, "handle_item_drop"):
            self.parent_game.handle_item_drop(source_widget, filename)

        event.acceptProposedAction()


class DragDropBrown(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.correct_items = ["cookie.png", "basket.png", "chocolate.png"]
        self.REQUIRED_CORRECT_COUNT = 3
        self.current_correct_count = 0
        self.score_logged = False  # Prevent duplicate logging per run

        self.audio_output = QAudioOutput(self)
        self.audio_player = QMediaPlayer(self)
        self.audio_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.8)

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

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

        pagsasanay = QLabel("Pagsasanay: Kayumanggi")
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

        self.items_row = QHBoxLayout()
        self.items_row.setSpacing(80)
        self.items_row.setContentsMargins(0, 0, 0, 20)
        self.items_row.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(self.items_row)

        self.drop_box = DropBox(
            os.path.join(IMAGE_DIR, "brown_box.png"), parent_game=self
        )
        main_layout.addWidget(self.drop_box, alignment=Qt.AlignCenter)

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

        self.item_images = ["cookie.png", "basket.png", "chocolate.png", "tv.png"]
        self.active_icons = []
        self.setup_items()

        main_layout.addStretch()

    def setup_items(self):
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
        sound_path = os.path.join(SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            abs_path = os.path.abspath(sound_path)
            self.audio_player.setSource(QUrl.fromLocalFile(abs_path))
            self.audio_player.play()

    def handle_item_drop(self, source_widget: DraggableIcon, filename: str):
        if filename in self.correct_items:
            self.current_correct_count += 1
            if source_widget in self.active_icons:
                self.active_icons.remove(source_widget)
            source_widget.deleteLater()

            if self.current_correct_count >= self.REQUIRED_CORRECT_COUNT:
                self.feedback_label.setText("✅ MAGALING! TAMA LAHAT!")
                self.feedback_label.setStyleSheet(
                    f"font-size: 26px; color: green; font-family: {BODY_FONT}; font-weight: bold;"
                )
                self.play_sound("correct.wav")
                self.restart_btn.show()
                self.next_btn.show()

                # --- AUTOMATIC SCORE LOGGING ---
                if not self.score_logged:
                    student_id = AppSession.get_active_student_id()
                    if student_id:
                        log_activity(
                            student_id=student_id,
                            module_name="Kulay",
                            target_word="Kayumanggi",
                            score=100.0
                        )
                        print("--> Kayumanggi game score successfully logged for active student!")
                        self.score_logged = True
            else:
                self.feedback_label.setText("Tama! Isa pa!")
                self.feedback_label.setStyleSheet(
                    f"font-size: 24px; color: green; font-family: {BODY_FONT}; font-weight: bold;"
                )
                self.play_sound("correct.wav")
        else:
            self.play_sound("wrong.wav")
            self.feedback_label.setText(
                "❌ SUBUKAN ULIT! Maling kulay! Na-reset ang laro."
            )
            self.feedback_label.setStyleSheet(
                f"font-size: 24px; color: red; font-family: {BODY_FONT}; font-weight: bold;"
            )
            self.reset_game()

    def reset_game(self):
        self.current_correct_count = 0
        self.score_logged = False
        self.restart_btn.hide()
        self.next_btn.hide()
        self.setup_items()

    def showEvent(self, event):
        self.reset_game()
        self.feedback_label.setText("")
        self.play_instruction_sound()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("kayumanggi")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("itim")

    def play_instruction_sound(self):
        sound_path = os.path.abspath(os.path.join(INSTRUCTION_SOUNDS_DIR, INSTRUCTION_SOUND_FILE))
        if os.path.exists(sound_path):
            self.instruction_player.stop()
            self.instruction_player.setSource(QUrl.fromLocalFile(sound_path))
            self.instruction_player.play()
        else:
            print(f"Instruction sound not found: {sound_path}")

    def stop_instruction_sound(self):
        self.instruction_player.stop()