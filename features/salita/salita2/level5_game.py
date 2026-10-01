import os
from PySide6.QtCore import Qt, QPoint, QSize, QUrl
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "salita")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "sounds", "correct_&_wrong")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "audio", "Salita")
INSTRUCTION_SOUND_FILE = "Magkatunog.mp3" 



class Dot(QLabel):
    def __init__(self, is_source: bool, item_id: str, parent_game):
        super().__init__()
        self.is_source = is_source
        self.item_id = item_id
        self.game = parent_game

        self.setFixedSize(20, 20)
        self.setStyleSheet(f"background-color: {CHOCO_BROWN}; border-radius: 10px;")
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


class Salita5Game(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.connections = []   # (source_dot, target_dot, is_correct)
        self.dragging_from = None
        self.temp_end_point = None
        self.total_pairs = 5

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

        # Top Bar
        top_bar = QHBoxLayout()
        back_btn = QPushButton()
        back_icon_path = os.path.join(ICONS_DIR, "back_arrow.png")
        if os.path.exists(back_icon_path):
            back_btn.setIcon(QIcon(back_icon_path))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(30, 30))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: transparent;")
        back_btn.clicked.connect(self.handle_back)
        top_bar.addWidget(back_btn)

        title = QLabel("Pagsasanay 5: Salitang Magkatugma")
        title.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Matching items layout
        rows_layout = QVBoxLayout()
        rows_layout.setSpacing(30)
        rows_layout.setContentsMargins(60, 20, 60, 10)
        main_layout.addLayout(rows_layout)

        items = [
            ("bola.png", "bola", "lola", "lola.png", "lola", "lola"),
            ("mata.png", "mata", "bata", "bata.png", "bata", "bata"),
            ("buto.png", "buto", "bato", "bato.png", "bato", "bato"),
            ("lapis.png", "lapis", "ipis", "ipis.png", "ipis", "ipis"),
            ("sako.png", "sako", "siko", "braso.png", "siko", "siko"),
        ]

        for left_img, left_txt, left_key, right_img, right_txt, right_key in items:
            row = QHBoxLayout()

            # Left side
            left_image_lbl = QLabel()
            left_path = os.path.join(IMAGE_DIR, left_img)
            if os.path.exists(left_path):
                left_image_lbl.setPixmap(
                    QPixmap(left_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            row.addWidget(left_image_lbl)

            left_word_lbl = QLabel(left_txt)
            left_word_lbl.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
            row.addWidget(left_word_lbl)

            source_dot = Dot(is_source=True, item_id=left_key, parent_game=self)
            row.addWidget(source_dot)

            row.addStretch()

            # Right side
            target_dot = Dot(is_source=False, item_id=right_key, parent_game=self)
            row.addWidget(target_dot)

            right_image_lbl = QLabel()
            right_path = os.path.join(IMAGE_DIR, right_img)
            if os.path.exists(right_path):
                right_image_lbl.setPixmap(
                    QPixmap(right_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            row.addWidget(right_image_lbl)

            right_word_lbl = QLabel(right_txt)
            right_word_lbl.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {CHOCO_BROWN}; font-family: {BODY_FONT};")
            row.addWidget(right_word_lbl)

            rows_layout.addLayout(row)

        # Action Buttons Layout
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

    def play_feedback_sound(self, is_correct: bool):
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
            self.feedback_player.stop()
            self.feedback_player.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
            self.feedback_player.play()

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
        is_correct = (source_dot.item_id == target_dot.item_id)
        self.play_feedback_sound(is_correct)

        self.connections = [c for c in self.connections if c[0] != source_dot]
        self.connections.append((source_dot, target_dot, is_correct))

        self.dragging_from = None
        self.temp_end_point = None
        self.update()

        self.restart_btn.show()

        if sum(1 for _, _, ok in self.connections if ok) == self.total_pairs:
            self.next_btn.show()

    def dot_center(self, dot: Dot) -> QPoint:
        return dot.mapTo(self, dot.rect().center())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for source_dot, target_dot, is_correct in self.connections:
            line_color = QColor("#2ECC71") if is_correct else QColor("#E74C3C")
            pen = QPen(line_color, 5)
            painter.setPen(pen)
            painter.drawLine(self.dot_center(source_dot), self.dot_center(target_dot))

        if self.dragging_from and self.temp_end_point:
            pen = QPen(QColor(MAGENTA), 5)
            painter.setPen(pen)
            painter.drawLine(self.dot_center(self.dragging_from), self.temp_end_point)

    def reset_game(self):
        self.connections.clear()
        self.dragging_from = None
        self.temp_end_point = None
        self.restart_btn.hide()
        self.next_btn.hide()
        self.update()

    def showEvent(self, event):
        self.reset_game()
        super().showEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("salita")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("salitaq6")

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