import os
from PySide6.QtCore import QMimeData, QPoint, QSize, Qt, Signal, QUrl
from PySide6.QtGui import QDrag, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from themes.colors import *
from themes.fonts import BODY_FONT
from session import AppSession
from Database.queries import log_activity

# Resolve project root directory safely
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image_content", "pnk")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "Vs PNK")
INSTRUCTION_SOUND_FILE = "PNK Instruction.mp3"


class DraggableWord(QLabel):
    """A word from the word bank that the user can drag onto a blank."""

    def __init__(self, display_text: str):
        super().__init__(display_text)
        self.display_text = display_text
        self.drag_start_position = QPoint()
        self.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                font-weight: 800;
                color: {CHOCO_BROWN};
                font-family: {BODY_FONT};
                background-color: #FFFDF8;
                border: 2px solid #D9CBB0;
                border-radius: 8px;
                padding: 6px 16px;
            }}
            QLabel:hover {{
                background-color: #F5E9D3;
            }}
        """)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton) or not self.isVisible():
            return

        if (
            event.pos() - self.drag_start_position
        ).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.display_text)
        drag.setMimeData(mime_data)

        drag.setPixmap(self.grab())
        drag.setHotSpot(event.pos())

        self.setCursor(Qt.ClosedHandCursor)
        drag.exec(Qt.CopyAction | Qt.MoveAction)
        self.setCursor(Qt.OpenHandCursor)


class LabelDropBox(QFrame):
    """An interactive target box that validates placed words."""

    word_changed = Signal()

    def __init__(
        self,
        target_word: str,
        border_color: str = "#3A2E1F",
        width=180,
        height=70,
    ):
        super().__init__()
        self.target_word = target_word
        self.default_border_color = border_color
        self.current_word = ""

        self.setAcceptDrops(True)
        self.setFixedSize(width, height)
        self.reset_style()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.answer_label = QLabel("")
        self.answer_label.setAlignment(Qt.AlignCenter)
        self.answer_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {CHOCO_BROWN};
            border: none;
            font-family: {BODY_FONT};
        """)
        layout.addWidget(self.answer_label)

    def reset_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(255, 255, 255, 0.6);
                border: 4px solid {self.default_border_color};
                border-radius: 12px;
            }}
        """)

    def set_correct_style(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border: 4px solid #2E7D32;
                border-radius: 12px;
            }
        """)

    def set_incorrect_style(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #FFEBEE;
                border: 4px solid #D32F2F;
                border-radius: 12px;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        dropped_text = event.mimeData().text()
        self.current_word = dropped_text
        self.answer_label.setText(dropped_text)

        if dropped_text.lower() == self.target_word.lower():
            self.set_correct_style()
        else:
            self.set_incorrect_style()

        event.acceptProposedAction()
        self.word_changed.emit()

    def mousePressEvent(self, event):
        """Clicking a filled box clears it."""
        if event.button() == Qt.LeftButton and self.current_word:
            self.current_word = ""
            self.answer_label.setText("")
            self.reset_style()
            self.word_changed.emit()


class PaaGame(QWidget):

    def __init__(self, router):
        super().__init__()
        self.router = router
        self.score_logged = False  # Prevent duplicate logging per run

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        # Top Bar
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(20, 20, 20, 10)
        top_bar.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter
        )

        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent;")
        back_btn.clicked.connect(self.handle_back)
        top_bar.addWidget(back_btn)

        title = QLabel("Pagsasanay 3: Paa, Tuhod, Binti")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            font-family: {BODY_FONT};
        """)
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Word Bank Container
        word_bank = QFrame()
        word_bank.setStyleSheet("""
            QFrame {
                background-color: #FAF4E8;
                border: 2px dashed #D9CBB0;
                border-radius: 12px;
            }
        """)
        word_bank_row = QHBoxLayout(word_bank)
        word_bank_row.setContentsMargins(30, 15, 30, 15)
        word_bank_row.setSpacing(30)
        word_bank_row.setAlignment(Qt.AlignCenter)

        words = ["balikat", "binti", "paa", "bibig", "braso", "tuhod"]
        for word_text in words:
            word_widget = DraggableWord(word_text)
            word_bank_row.addWidget(word_widget)

        main_layout.addWidget(word_bank)

        # Diagram Layout
        diagram_layout = QHBoxLayout()
        diagram_layout.setAlignment(Qt.AlignCenter)
        diagram_layout.setSpacing(40)
        main_layout.addLayout(diagram_layout)

        first_column = QVBoxLayout()
        first_column.setSpacing(25)
        first_column.setAlignment(Qt.AlignCenter)
        diagram_layout.addLayout(first_column)

        self.binti_db = LabelDropBox(
            target_word="binti", border_color=SKY_BLUE
        )
        self.paa_db = LabelDropBox(
            target_word="paa", border_color=ELECTRIC_VIOLET
        )
        self.tuhod_db = LabelDropBox(
            target_word="tuhod", border_color=SCARLET
        )

        first_column.addWidget(self.binti_db)
        first_column.addWidget(self.paa_db)
        first_column.addWidget(self.tuhod_db)

        # Image Display
        self.body_image = QLabel()
        image_path = os.path.join(IMAGE_DIR, "paa.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                380, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.body_image.setPixmap(pixmap)
        self.body_image.setAlignment(Qt.AlignCenter)
        diagram_layout.addWidget(self.body_image)

        # Drop Box Completion Monitoring
        self.drop_boxes = [self.binti_db, self.paa_db, self.tuhod_db]
        for db in self.drop_boxes:
            db.word_changed.connect(self.check_completion)

        # Bottom Action Bar
        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)

        self.next_btn = QPushButton("Tapusin ➔")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2E7D32;
                color: white;
                font-family: {BODY_FONT};
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px 36px;
            }}
            QPushButton:hover {{
                background-color: #1B5E20;
            }}
            QPushButton:disabled {{
                background-color: #BDBDBD;
                color: #757575;
            }}
        """)
        self.next_btn.clicked.connect(self.handle_next)
        action_layout.addWidget(self.next_btn)
        main_layout.addLayout(action_layout)

        # Initial completion check
        self.check_completion()

    def check_completion(self):
        """Enables Tapusin button only when all diagram labels are correctly answered."""
        all_correct = all(
            db.current_word.lower() == db.target_word.lower()
            for db in self.drop_boxes
        )
        self.next_btn.setEnabled(all_correct)

        if all_correct and not self.score_logged:
            student_id = AppSession.get_active_student_id()
            if student_id:
                log_activity(
                    student_id=student_id,
                    module_name="Parte ng Katawan",
                    target_word="Paa",
                    score=100.0
                )
                print("--> Paa game score successfully logged for active student!")
                self.score_logged = True

    def handle_back(self):
        self.score_logged = False
        self.router.navigate("paa")

    def handle_next(self):
        self.score_logged = False
        self.router.navigate("katawan")

    def showEvent(self, event):
        self.score_logged = False
        self.play_instruction_sound()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

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