import os
from PySide6.QtCore import Qt, QMimeData, QSize, QUrl
from PySide6.QtGui import QDrag, QPixmap, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from themes.fonts import BODY_FONT
from themes.colors import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "bilang_g1")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong")


class DraggableWord(QLabel):
    """A picture from the picture bank that the user can drag onto a blank."""

    def __init__(self, word_id: str, image_path: str, parent_game, size: int = 150):
        super().__init__()
        self.word_id = word_id
        self.image_path = image_path
        self.game = parent_game

        pixmap = QPixmap(image_path).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(160, 160)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self.isVisible():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.word_id)
        mime_data.setProperty("image_path", self.image_path)

        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos())

        # Executing move action and hiding from bank if successful
        result = drag.exec(Qt.MoveAction)
        if result == Qt.MoveAction:
            self.hide()


class BlankDropTarget(QLabel):
    """An underlined image drop target inside the exercise."""

    def __init__(self, target_id: str, parent_game, size: int = 180):
        super().__init__("")
        self.target_id = target_id
        self.game = parent_game
        self.target_size = size
        self.placed_word_id = None
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self.reset_style()

    def reset_style(self):
        self.clear()
        self.placed_word_id = None
        self.setStyleSheet(f"""
            border: 2px dashed {CHOCO_BROWN};
            border-radius: 10px;
            background-color: transparent;
        """)

    def apply_feedback_style(self, is_correct: bool):
        border_color = "#2ECC71" if is_correct else "#E74C3C"
        bg_color = "#EAFAF1" if is_correct else "#FDEDEC"
        self.setStyleSheet(f"""
            border: 4px solid {border_color};
            border-radius: 10px;
            background-color: {bg_color};
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Return existing picture to the bank if overwriting
        if self.placed_word_id:
            self.game.return_picture_to_bank(self.placed_word_id)

        dropped_id = event.mimeData().text()
        image_path = event.mimeData().property("image_path")

        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                self.target_size - 20,
                self.target_size - 20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(pixmap)
            self.placed_word_id = dropped_id
            self.setStyleSheet(f"""
                border: 2px solid {CHOCO_BROWN};
                border-radius: 10px;
                background-color: {PASTEL_YELLOW};
            """)

            # Signal move action to caller
            event.setDropAction(Qt.MoveAction)
            event.accept()

            self.game.check_completion()

    def mousePressEvent(self, event):
        # Click filled blank to return picture to bank
        if event.button() == Qt.LeftButton and self.placed_word_id:
            self.game.return_picture_to_bank(self.placed_word_id)
            self.reset_style()
            self.game.check_completion()


class BilangLvl5(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Correct skip-counting sequence (2, 4, 6, 8, 10)
        self.correct_answers = {
            "blank1": "apat",
            "blank2": "anim",
            "blank3": "sampu"
        }

        self.picture_widgets = {}

        # Audio Setup
        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(0.8)

        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(25)

        # Top Bar Navigation
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(60, 50, 0, 20)
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)

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

        title = QLabel("Pagsasanay 5: Dalawahang Pagbilang")
        title.setStyleSheet(f"font-size: 30px; font-weight: 600; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Picture Bank Frame
        pic_bank = QFrame()
        pic_bank.setMinimumWidth(800)
        pic_bank.setStyleSheet("border: 1px solid #D9CBB0; border-radius: 8px; background-color: #FFFDF5;")

        pic_bank_row = QHBoxLayout(pic_bank)
        pic_bank_row.setContentsMargins(20, 20, 20, 20)
        pic_bank_row.setSpacing(40)
        pic_bank_row.addStretch(1)

        items = [
            ("apat", "4pencil.png"),
            ("anim", "6pencil.png"),
            ("sampu", "10pencil.png")
        ]

        for word_id, image_file in items:
            img_path = os.path.join(IMAGE_DIR, image_file)
            pic_widget = DraggableWord(word_id, img_path, self, size=140)
            self.picture_widgets[word_id] = pic_widget
            pic_bank_row.addWidget(pic_widget)

        pic_bank_row.addStretch(1)
        main_layout.addWidget(pic_bank)

        # Exercise Image Sequence Layout (2, blank1, blank2, 8, blank3)
        image_layout = QHBoxLayout()
        image_layout.setSpacing(15)
        image_layout.setAlignment(Qt.AlignCenter)

        dalawa = QLabel()
        dalawa.setAlignment(Qt.AlignCenter)
        dalawa_path = os.path.join(IMAGE_DIR, "2pencil.png")
        if os.path.exists(dalawa_path):
            dalawa.setPixmap(
                QPixmap(dalawa_path).scaled(
                    180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        image_layout.addWidget(dalawa)

        self.blank1 = BlankDropTarget("blank1", self, size=180)
        image_layout.addWidget(self.blank1)

        self.blank2 = BlankDropTarget("blank2", self, size=180)
        image_layout.addWidget(self.blank2)

        walo = QLabel()
        walo.setAlignment(Qt.AlignCenter)
        walo_path = os.path.join(IMAGE_DIR, "8pencil.png")
        if os.path.exists(walo_path):
            walo.setPixmap(
                QPixmap(walo_path).scaled(
                    180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        image_layout.addWidget(walo)

        self.blank3 = BlankDropTarget("blank3", self, size=180)
        image_layout.addWidget(self.blank3)

        main_layout.addLayout(image_layout)

        # Action Buttons Layout (Restart + Next)
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

        main_layout.addStretch()

    def return_picture_to_bank(self, word_id: str):
        if word_id in self.picture_widgets:
            self.picture_widgets[word_id].show()

    def play_feedback_sound(self, is_correct: bool):
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.stop()
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

    def check_completion(self):
        val1 = self.blank1.placed_word_id
        val2 = self.blank2.placed_word_id
        val3 = self.blank3.placed_word_id

        if val1 or val2 or val3:
            self.restart_btn.show()

        if val1 and val2 and val3:
            is_b1_ok = (val1 == self.correct_answers["blank1"])
            is_b2_ok = (val2 == self.correct_answers["blank2"])
            is_b3_ok = (val3 == self.correct_answers["blank3"])

            all_correct = is_b1_ok and is_b2_ok and is_b3_ok

            self.blank1.apply_feedback_style(is_b1_ok)
            self.blank2.apply_feedback_style(is_b2_ok)
            self.blank3.apply_feedback_style(is_b3_ok)

            self.play_feedback_sound(all_correct)

            if all_correct:
                self.next_btn.show()
            else:
                self.next_btn.hide()

    def reset_game(self):
        self.blank1.reset_style()
        self.blank2.reset_style()
        self.blank3.reset_style()

        for widget in self.picture_widgets.values():
            widget.show()

        self.restart_btn.hide()
        self.next_btn.hide()

    def showEvent(self, event):
        self.reset_game()
        super().showEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("bilang_g1")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("dalawahan_q2")