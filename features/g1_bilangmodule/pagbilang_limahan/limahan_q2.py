import os
from PySide6.QtCore import Qt, QMimeData, QSize, QUrl
from PySide6.QtGui import QDrag, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from themes.fonts import BODY_FONT
from themes.colors import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "G1 Bilang")
INSTRUCTION_SOUND_FILE = "TANONG 6.mp3" 



class DraggableWord(QLabel):
    """A number label from the number bank that the user can drag onto a blank."""

    def __init__(self, display_text: str, parent_game):
        super().__init__(display_text)
        self.word_text = display_text
        self.game = parent_game

        self.setStyleSheet(f"""
            font-size: 50px;
            font-weight: 700;
            color: {CHOCO_BROWN};
            font-family: {BODY_FONT};
            background-color: {SKY_BLUE};
            border-radius: 12px;
        """)
        self.setFixedSize(100, 80)
        self.setCursor(Qt.OpenHandCursor)
        self.setAlignment(Qt.AlignCenter)

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
    """An underlined blank inside the exercise that accepts dragged numbers."""

    def __init__(self, target_id: str, parent_game, min_width: int = 120):
        super().__init__("")
        self.target_id = target_id
        self.game = parent_game
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(min_width)
        self.setFixedHeight(90)
        self.setCursor(Qt.PointingHandCursor)
        self.reset_style()

    def reset_style(self):
        self.setText("")
        self.setStyleSheet(f"""
            font-size: 50px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            border: none;
            border-bottom: 4px solid {CHOCO_BROWN};
            background-color: transparent;
            font-family: {BODY_FONT};
        """)

    def apply_feedback_style(self, is_correct: bool):
        bg_color = "#2ECC71" if is_correct else "#E74C3C"
        self.setStyleSheet(f"""
            font-size: 50px;
            font-weight: 800;
            color: white;
            border: none;
            border-radius: 12px;
            background-color: {bg_color};
            font-family: {BODY_FONT};
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.text():
            self.game.return_number_to_bank(self.text())

        dropped_text = event.mimeData().text()
        self.setText(dropped_text)
        self.setStyleSheet(f"""
            font-size: 50px;
            font-weight: 800;
            color: {CHOCO_BROWN};
            border: none;
            border-bottom: 4px solid {CHOCO_BROWN};
            background-color: {SKY_BLUE};
            font-family: {BODY_FONT};
        """)

        event.setDropAction(Qt.MoveAction)
        event.accept()

        self.game.check_completion()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.text():
            self.game.return_number_to_bank(self.text())
            self.reset_style()
            self.game.check_completion()


class BilangLvl8(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Correct skip-counting sequence answers (30, 35, 40, 45, 50, 55, 60, 65)
        self.correct_answers = {
            "blank1": "30",
            "blank2": "40",
            "blank3": "45",
            "blank4": "60",
            "blank5": "65"
        }

        self.number_widgets = {}

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

        title = QLabel("Pagsasanay 8: Limahang Pagbilang")
        title.setStyleSheet(f"font-size: 30px; font-weight: 600; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Numbers Bank Frame
        word_bank = QFrame()
        word_bank.setMinimumWidth(600)
        word_bank.setStyleSheet("border: 1px solid #D9CBB0; border-radius: 8px; background-color: #FFFDF5;")

        word_bank_row = QHBoxLayout(word_bank)
        word_bank_row.setContentsMargins(20, 20, 20, 20)
        word_bank_row.setSpacing(40)
        word_bank_row.setAlignment(Qt.AlignCenter)

        numbers = ["30", "40", "45", "60", "65"]
        for num_text in numbers:
            num_widget = DraggableWord(num_text, self)
            self.number_widgets[num_text] = num_widget
            word_bank_row.addWidget(num_widget)

        main_layout.addWidget(word_bank)

        # Number Sequence Lines
        sentence_layout = QVBoxLayout()
        sentence_layout.setSpacing(40)
        sentence_layout.setAlignment(Qt.AlignCenter)

        # First Line: [blank1]  35  [blank2]  [blank3]
        first_line = QHBoxLayout()
        first_line.setSpacing(50)
        first_line.setAlignment(Qt.AlignCenter)

        self.blank1 = BlankDropTarget("blank1", self, min_width=120)
        first_line.addWidget(self.blank1)

        first_num = QLabel("35")
        first_num.setStyleSheet(f"font-size: 70px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        first_line.addWidget(first_num)

        self.blank2 = BlankDropTarget("blank2", self, min_width=120)
        first_line.addWidget(self.blank2)

        self.blank3 = BlankDropTarget("blank3", self, min_width=120)
        first_line.addWidget(self.blank3)

        sentence_layout.addLayout(first_line)

        # Second Line: 50  55  [blank4]  [blank5]
        second_line = QHBoxLayout()
        second_line.setSpacing(50)
        second_line.setAlignment(Qt.AlignCenter)

        second_num = QLabel("50")
        second_num.setStyleSheet(f"font-size: 70px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        second_line.addWidget(second_num)

        third_num = QLabel("55")
        third_num.setStyleSheet(f"font-size: 70px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        second_line.addWidget(third_num)

        self.blank4 = BlankDropTarget("blank4", self, min_width=120)
        second_line.addWidget(self.blank4)

        self.blank5 = BlankDropTarget("blank5", self, min_width=120)
        second_line.addWidget(self.blank5)

        sentence_layout.addLayout(second_line)
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

    def return_number_to_bank(self, num_text: str):
        if num_text in self.number_widgets:
            self.number_widgets[num_text].show()

    def play_feedback_sound(self, is_correct: bool):
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.stop()
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

    def check_completion(self):
        v1 = self.blank1.text().strip()
        v2 = self.blank2.text().strip()
        v3 = self.blank3.text().strip()
        v4 = self.blank4.text().strip()
        v5 = self.blank5.text().strip()

        if v1 or v2 or v3 or v4 or v5:
            self.restart_btn.show()

        if v1 and v2 and v3 and v4 and v5:
            is_b1_ok = (v1 == self.correct_answers["blank1"])
            is_b2_ok = (v2 == self.correct_answers["blank2"])
            is_b3_ok = (v3 == self.correct_answers["blank3"])
            is_b4_ok = (v4 == self.correct_answers["blank4"])
            is_b5_ok = (v5 == self.correct_answers["blank5"])

            all_correct = is_b1_ok and is_b2_ok and is_b3_ok and is_b4_ok and is_b5_ok

            self.blank1.apply_feedback_style(is_b1_ok)
            self.blank2.apply_feedback_style(is_b2_ok)
            self.blank3.apply_feedback_style(is_b3_ok)
            self.blank4.apply_feedback_style(is_b4_ok)
            self.blank5.apply_feedback_style(is_b5_ok)

            self.play_feedback_sound(all_correct)

            if all_correct:
                self.next_btn.show()
            else:
                self.next_btn.hide()

    def reset_game(self):
        self.blank1.reset_style()
        self.blank2.reset_style()
        self.blank3.reset_style()
        self.blank4.reset_style()
        self.blank5.reset_style()

        for widget in self.number_widgets.values():
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
        self.router.navigate("pagdaragdag")

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