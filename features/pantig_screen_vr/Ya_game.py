import os
from PySide6.QtCore import Qt, QPoint, QSize, QUrl
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
from themes.colors import *
from themes.fonts import BODY_FONT
from session import AppSession
from Database.queries import log_activity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "image_content", "pantig")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "icons")
FEEDBACK_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "sounds", "correct_&_wrong")
INSTRUCTION_SOUNDS_DIR = os.path.join(BASE_DIR, "..", "..", "assets", "audio", "VS Pantig")
INSTRUCTION_SOUND_FILE = "Game Instruction Pantig.mp3" 



class Dot(QLabel):
    def __init__(self, dot_id: str, is_source: bool, parent_game):
        super().__init__()
        self.dot_id = dot_id
        self.is_source = is_source
        self.game = parent_game

        self.setFixedSize(20, 20)
        self.setStyleSheet("background-color: #3A2E1F; border-radius: 10px;")
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


class MatchingYa(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        self.feedback_audio_output = QAudioOutput(self)
        self.feedback_player = QMediaPlayer(self)
        self.feedback_player.setAudioOutput(self.feedback_audio_output)
        self.feedback_audio_output.setVolume(0.8)

        self.instruction_audio_output = QAudioOutput(self)
        self.instruction_player = QMediaPlayer(self)
        self.instruction_player.setAudioOutput(self.instruction_audio_output)
        self.instruction_audio_output.setVolume(0.9)

        self.connections = []
        self.dragging_from = None
        self.temp_end_point = None
        self.score_logged = False  # Prevent duplicate logs in a single run

        self.correct_pairs = {
            "footprint": "yapak",
            "maid": "yaya",
            "yacht": "yate"
        }

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)

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
        back_btn.setStyleSheet("border: none; background-color: transparent; border-radius: 6px;")
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

        rows_layout = QVBoxLayout()
        rows_layout.setSpacing(40)
        rows_layout.setContentsMargins(80, 40, 80, 20)
        main_layout.addLayout(rows_layout)

        items = [
            ("footprint", "yapak.png", "yate", "Ya-te"),
            ("maid", "yaya.png", "yapak", "Ya-pak"),
            ("yacht", "yate.png", "yaya", "Ya-ya"),
        ]

        for image_id, image_file, word_id, word_display in items:
            row = QHBoxLayout()

            image_label = QLabel()
            img_path = os.path.join(IMAGE_DIR, image_file)
            if os.path.exists(img_path):
                image_label.setPixmap(
                    QPixmap(img_path).scaled(
                        140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                )
            row.addWidget(image_label)

            source_dot = Dot(image_id, is_source=True, parent_game=self)
            row.addWidget(source_dot)

            row.addStretch()

            target_dot = Dot(word_id, is_source=False, parent_game=self)
            row.addWidget(target_dot)

            word_label = QLabel(word_display)
            word_label.setStyleSheet(f"font-size: 46px; font-family:{BODY_FONT}; font-weight: 800; color: #3A2E1F;")
            row.addWidget(word_label)

            rows_layout.addLayout(row)

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

    def reset_game(self):
        self.connections.clear()
        self.dragging_from = None
        self.temp_end_point = None
        self.score_logged = False
        self.restart_btn.hide()
        self.next_btn.hide()
        self.update()

    def showEvent(self, event):
        self.reset_game()
        self.play_instruction_sound()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_instruction_sound()
        super().hideEvent(event)

    def handle_back(self):
        self.reset_game()
        self.router.navigate("yaya")

    def handle_next(self):
        self.reset_game()
        self.router.navigate("pantig")

    def play_feedback_sound(self, is_correct: bool):
        filename = "correct.wav" if is_correct else "wrong.wav"
        sound_path = os.path.join(FEEDBACK_SOUNDS_DIR, filename)
        if os.path.exists(sound_path):
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
        self.connections = [c for c in self.connections if c[0] != source_dot]
        
        is_correct = self.correct_pairs.get(source_dot.dot_id) == target_dot.dot_id
        self.connections.append((source_dot, target_dot, is_correct))

        self.play_feedback_sound(is_correct)

        self.dragging_from = None
        self.temp_end_point = None
        self.restart_btn.show()

        if len(self.connections) == len(self.correct_pairs) and all(c[2] for c in self.connections):
            self.next_btn.show()

            # --- AUTOMATIC SCORE LOGGING ---
            if not self.score_logged:
                student_id = AppSession.get_active_student_id()
                if student_id:
                    correct_count = sum(1 for c in self.connections if c[2])
                    total_items = len(self.correct_pairs)
                    score_percentage = (correct_count / total_items) * 100
                    
                    log_activity(
                        student_id=student_id,
                        module_name="Pantig",
                        target_word="Ya",
                        score=score_percentage
                    )
                    print("--> Matching Ya game score successfully logged for active student!")
                    self.score_logged = True

        self.update()

    def dot_center(self, dot: Dot) -> QPoint:
        return dot.mapTo(self, dot.rect().center())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for conn in self.connections:
            source_dot, target_dot = conn[0], conn[1]
            is_correct = conn[2] if len(conn) > 2 else True

            color_hex = "#2ECC71" if is_correct else "#E74C3C"
            pen = QPen(QColor(color_hex), 8)
            painter.setPen(pen)
            painter.drawLine(self.dot_center(source_dot), self.dot_center(target_dot))

        if self.dragging_from and self.temp_end_point:
            pen = QPen(QColor("#FFD24C"), 8)
            painter.setPen(pen)
            painter.drawLine(self.dot_center(self.dragging_from), self.temp_end_point)

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