import os

from features.voice_recog import OfflineVoiceWorker
from PySide6.QtCore import QSize, Qt, QUrl, Slot, QMimeData
from PySide6.QtGui import QIcon, QPixmap, QDrag
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
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
    """A word the user can drag (e.g. 'Isa', 'Lima', 'Tatlo')."""
 
    def __init__(self, display_text: str):
        super().__init__(display_text)
        self.setStyleSheet(f"""
            font-size: 50px;
            font-weight: 800;
            font-family: {BODY_FONT};
            color: {CHOCO_BROWN};
        """)
        self.setCursor(Qt.OpenHandCursor)
 
    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
 
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())   # carry the word's text along with the drag
        drag.setMimeData(mime_data)
 
        drag.setPixmap(self.grab())      # drag "ghost" looks like the label itself
        drag.setHotSpot(event.pos())
 
        drag.exec(Qt.MoveAction)
 
 
class AnswerDropBox(QFrame):
    """The empty box — accepts any dropped word, no validation."""
 
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedSize(400, 100)
        self.setFrameShape(QFrame.NoFrame)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet(f"""
            AnswerDropBox {{
                background-color: none;
                border: 2px solid {CHOCO_BROWN};
                border-radius: 10px;
            }}
            QLabel {{
                border: none;
            }}
        """)
 
        layout = QVBoxLayout(self)
        self.answer_label = QLabel("")
        layout.setContentsMargins(0, 0, 0, 0)
        self.answer_label.setAlignment(Qt.AlignCenter)
        self.answer_label.setStyleSheet(f"font-size: 50px; font-family: {BODY_FONT}; font-weight: 800; color: {CHOCO_BROWN};")
        layout.addWidget(self.answer_label)
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
 
    def dropEvent(self, event):
        dropped_text = event.mimeData().text()
        self.answer_label.setText(dropped_text)  
        event.acceptProposedAction()
 
 
class IsaGame(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.current_number = 1
 
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
        back_btn.clicked.connect(lambda: self.router.navigate("1"))

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
 
        # Row of draggable word choices, inside a bordered container
        words_container = QFrame()
        words_container.setStyleSheet("border: 1px solid #D9CBB0; border-radius: 4px;")
        words_row = QHBoxLayout(words_container)
        words_row.setContentsMargins(30, 15, 30, 15)
        words_row.setSpacing(80)
 
        for display in ["Lima", "Isa", "Tatlo", "Dalawa"]:
            word = DraggableWord(display)
            words_row.addWidget(word)
            words_row.addStretch()
 
        main_layout.addWidget(words_container)
 
        # Question row: number + picture on the left, drop box on the right
        question_row = QHBoxLayout()
        question_row.setSpacing(10)
        question_row.setContentsMargins(0, 20, 0, 0)
 

        #Picture group
        picture_group = QWidget()
        picture_group_layout = QHBoxLayout(picture_group)
        picture_group_layout.setContentsMargins(0, 0, 0, 0)
        picture_group_layout.setSpacing(10)
 
        for _ in range(self.current_number):
            single_picture = QLabel()
            single_picture.setPixmap(
                QPixmap(os.path.join(IMAGE_DIR, "xmast.png")).scaled(
                    300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
            picture_group_layout.addWidget(single_picture)
 
        question_row.addWidget(picture_group)

        question_row.addSpacing(80)
 
        self.drop_box = AnswerDropBox()
        question_row.addWidget(self.drop_box)

        question_row.addStretch()
 
        main_layout.addLayout(question_row)
 