import os

from PySide6.QtCore import QPoint, QSize, Qt, QUrl, QMimeData
from PySide6.QtGui import QIcon, QPixmap, QDrag
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame
)
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image_content", "bilang")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(
    BASE_DIR, "assets", "sounds", "correct_&_wrong"
)


class DraggableWord(QLabel):
    def __init__(self, display_text: str):
        super().__init__(display_text)
        self.drag_start_position = QPoint()
        self.setStyleSheet(f"""
            font-size: 50px;
            font-weight: 800;
            font-family: {BODY_FONT};
            color: {CHOCO_BROWN};
            background-color: transparent;
        """)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)

        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())

        self.setCursor(Qt.ClosedHandCursor)
        drag.exec(Qt.CopyAction | Qt.MoveAction)
        self.setCursor(Qt.OpenHandCursor)


class AnswerDropBox(QFrame):
    def __init__(self, parent_game):
        super().__init__()
        self.game = parent_game
        self.setAcceptDrops(True)
        self.setFixedSize(400, 100)
        self.setFrameShape(QFrame.NoFrame)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.reset_style()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.answer_label = QLabel("")
        self.answer_label.setAlignment(Qt.AlignCenter)
        self.answer_label.setStyleSheet(
            f"font-size: 50px; font-family: {BODY_FONT}; font-weight: 800; color: {CHOCO_BROWN}; border: none;"
        )
        layout.addWidget(self.answer_label)

    def reset_style(self):
        self.setStyleSheet(f"""
            AnswerDropBox {{
                background-color: transparent;
                border: 2px dashed {CHOCO_BROWN};
                border-radius: 10px;
            }}
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.setStyleSheet(f"""
                AnswerDropBox {{
                    background-color: rgba(230, 230, 230, 0.5);
                    border: 3px solid {CHOCO_BROWN};
                    border-radius: 10px;
                }}
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if not self.answer_label.text():
            self.reset_style()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            dropped_text = event.mimeData().text()
            self.answer_label.setText(dropped_text)
            event.acceptProposedAction()
            self.game.on_answer_dropped()
        else:
            event.ignore()


class SampuGame(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.current_number = 10
        self.target_word = "Sampu"

        # Feedback Audio Player Setup
        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(0.8)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(25)

        # Top Navigation Bar
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_bar)

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

        instruction = QLabel("Bilangin ang mga larawan")
        instruction.setStyleSheet(f"font-size: 22px; color: {CHOCO_BROWN}; font-family: {BODY_FONT}")
        main_layout.addWidget(instruction)

        # Row of draggable word choices
        words_container = QFrame()
        words_container.setStyleSheet("border: 1px solid #D9CBB0; border-radius: 4px;")
        words_row = QHBoxLayout(words_container)
        words_row.setContentsMargins(30, 15, 30, 15)
        words_row.setSpacing(80)

        for display in ["Sampu", "Siyam", "Pito", "Walo"]:
            word = DraggableWord(display)
            words_row.addWidget(word)
            words_row.addStretch()

        main_layout.addWidget(words_container)

        # Question row
        question_row = QHBoxLayout()
        question_row.setAlignment(Qt.AlignCenter)
        question_row.setSpacing(50)
        question_row.setContentsMargins(0, 20, 0, 0)

        picture_group = QWidget()
        picture_group_layout = QGridLayout(picture_group)
        picture_group_layout.setContentsMargins(0, 0, 0, 0)
        picture_group_layout.setSpacing(10)

        araw_pixmap = QPixmap(os.path.join(IMAGE_DIR, "bat.png")).scaled(
            150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        max_item = 5

        for i in range(self.current_number):
            row = i // max_item
            col = i % max_item

            img_label = QLabel()
            img_label.setPixmap(araw_pixmap)
            picture_group_layout.addWidget(img_label, row, col)

        question_row.addWidget(picture_group)
        question_row.addSpacing(80)

        self.drop_box = AnswerDropBox(parent_game=self)
        question_row.addWidget(self.drop_box)
        question_row.addStretch()

        main_layout.addLayout(question_row)

        # Action Buttons Layout
        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.setSpacing(20)

        self.check_btn = QPushButton("Suriin")
        self.check_btn.setCursor(Qt.PointingHandCursor)
        self.check_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BRIGHT_YELLOW};
                color: {CHOCO_BROWN};
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
        self.check_btn.hide()
        self.check_btn.clicked.connect(self.check_answer)

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

        self.next_btn = QPushButton("Tapusin ➔")
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

        action_layout.addWidget(self.check_btn)
        action_layout.addWidget(self.restart_btn)
        action_layout.addWidget(self.next_btn)
        main_layout.addLayout(action_layout)

        main_layout.addStretch()

    def on_answer_dropped(self):
        self.check_btn.show()
        self.restart_btn.show()

    def check_answer(self):
        answer = self.drop_box.answer_label.text().strip()
        is_correct = (answer.lower() == self.target_word.lower())

        self.play_feedback_sound(is_correct)

        if is_correct:
            self.drop_box.setStyleSheet(f"""
                AnswerDropBox {{
                    background-color: transparent;
                    border: 4px solid #2ECC71;
                    border-radius: 10px;
                }}
            """)
            self.next_btn.show()
        else:
            self.drop_box.setStyleSheet(f"""
                AnswerDropBox {{
                    background-color: transparent;
                    border: 4px solid #E74C3C;
                    border-radius: 10px;
                }}
            """)

    def play_feedback_sound(self, is_correct: bool):
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

    def reset_game(self):
        self.drop_box.answer_label.setText("")
        self.drop_box.reset_style()
        self.check_btn.hide()
        self.restart_btn.hide()
        self.next_btn.hide()

    def showEvent(self, event):
        self.reset_game()
        super().showEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("10")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("bilang")