import os
from PySide6.QtCore import Qt, QMimeData, QSize, QUrl
from PySide6.QtGui import QDrag, QPixmap, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from themes.fonts import BODY_FONT
from themes.colors import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "salita")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "Salita")
INSTRUCTION_SOUND_FILE = "Pangungusap Instruction.mp3" 



class DraggableWord(QLabel):
    """A word label in the word bank that can be dragged into drop targets."""

    def __init__(self, display_text: str, parent_game):
        super().__init__(display_text)
        self.word_text = display_text
        self.game = parent_game

        self.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            font-family: {BODY_FONT};
            padding: 6px 14px;
            background-color: {PASTEL_YELLOW};
            border-radius: 8px;
        """)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self.isVisible():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.word_text)
        drag.setMimeData(mime_data)

        drag.setPixmap(self.grab())
        drag.setHotSpot(event.pos())

        result = drag.exec(Qt.MoveAction)
        if result == Qt.MoveAction:
            self.hide()


class BlankDropTarget(QLabel):
    """An underlined blank inside the sentence."""

    def __init__(self, target_id: str, parent_game, min_width: int = 180):
        super().__init__("")
        self.target_id = target_id
        self.game = parent_game
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(min_width)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.reset_style()

    def reset_style(self):
        self.setText("")
        self.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            border: none;
            border-bottom: 4px solid {CHOCO_BROWN};
            background-color: transparent;
        """)

    def apply_feedback_style(self, is_correct: bool):
        bg_color = "#2ECC71" if is_correct else "#E74C3C"
        self.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 800;
            color: white;
            border: none;
            border-radius: 8px;
            background-color: {bg_color};
            font-family: {BODY_FONT};
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.text():
            self.game.return_word_to_bank(self.text())

        dropped_text = event.mimeData().text()
        self.setText(dropped_text)
        self.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            border: none;
            border-radius: 8px;
            background-color: {PASTEL_YELLOW};
            font-family: {BODY_FONT};
        """)

        event.setDropAction(Qt.MoveAction)
        event.accept()

        self.game.check_completion()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.text():
            self.game.return_word_to_bank(self.text())
            self.reset_style()
            self.game.check_completion()


class Salita12Game(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.correct_answers = {
            "blank1": "bata",
            "blank2": "naglilinis"
        }

        self.word_widgets = {}

        # Audio Setup
        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(0.8)

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(25)

        # Top Bar
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

        title = QLabel("Pagsasanay 12: Pangungusap")
        title.setStyleSheet(f"font-size: 30px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Word Bank Container
        word_bank = QFrame()
        word_bank.setMinimumWidth(800)
        word_bank.setStyleSheet("border: 1px solid #D9CBB0; border-radius: 8px; background-color: #FFFDF5;")
        self.word_bank_row = QHBoxLayout(word_bank)
        self.word_bank_row.setContentsMargins(40, 15, 40, 15)
        self.word_bank_row.setSpacing(30)
        self.word_bank_row.setAlignment(Qt.AlignCenter)

        words = ["bata", "naglilinis", "naglalaro", "matanda", "nakain"]
        for word_text in words:
            word_widget = DraggableWord(word_text, self)
            self.word_widgets[word_text] = word_widget
            self.word_bank_row.addWidget(word_widget)

        main_layout.addWidget(word_bank)

        # Sentence & Illustration Container
        sentence_layout = QVBoxLayout()
        sentence_layout.setSpacing(20)

        picture_label = QLabel()
        picture_label.setAlignment(Qt.AlignCenter)
        image_path = os.path.join(IMAGE_DIR, "naglilinis.png")
        if os.path.exists(image_path):
            picture_label.setPixmap(
                QPixmap(image_path).scaled(
                    260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        sentence_layout.addWidget(picture_label)

        # Sentence Line: "Ang mga [blank1] ay [blank2] ."
        line1 = QHBoxLayout()
        line1.setAlignment(Qt.AlignCenter)
        line1.setSpacing(15)

        ang_label = QLabel("Ang mga")
        ang_label.setStyleSheet(f"font-size: 36px; font-weight: 800; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        line1.addWidget(ang_label)

        self.blank1 = BlankDropTarget("blank1", self, min_width=180)
        line1.addWidget(self.blank1)

        ay_label = QLabel("ay")
        ay_label.setStyleSheet(f"font-size: 36px; font-weight: 800; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        line1.addWidget(ay_label)

        self.blank2 = BlankDropTarget("blank2", self, min_width=220)
        line1.addWidget(self.blank2)

        period_label = QLabel(".")
        period_label.setStyleSheet(f"font-size: 36px; font-weight: 800; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        line1.addWidget(period_label)

        sentence_layout.addLayout(line1)
        main_layout.addLayout(sentence_layout)

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

        self.next_btn = QPushButton("Matapos ➔")
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

    def return_word_to_bank(self, word_text: str):
        if word_text in self.word_widgets:
            self.word_widgets[word_text].show()

    def play_feedback_sound(self, is_correct: bool):
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.stop()
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

    def check_completion(self):
        val1 = self.blank1.text().strip().lower()
        val2 = self.blank2.text().strip().lower()

        if val1 or val2:
            self.restart_btn.show()

        if val1 and val2:
            is_b1_ok = (val1 == self.correct_answers["blank1"])
            is_b2_ok = (val2 == self.correct_answers["blank2"])
            all_correct = is_b1_ok and is_b2_ok

            self.blank1.apply_feedback_style(is_b1_ok)
            self.blank2.apply_feedback_style(is_b2_ok)

            self.play_feedback_sound(all_correct)

            if all_correct:
                self.next_btn.show()
            else:
                self.next_btn.hide()

    def reset_game(self):
        self.blank1.reset_style()
        self.blank2.reset_style()

        for widget in self.word_widgets.values():
            widget.show()

        self.restart_btn.hide()
        self.next_btn.hide()

    def showEvent(self, event):
        self.reset_game()
        super().showEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("salita")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("salita")

    def showEvent(self, event):
        self.reset_game()
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