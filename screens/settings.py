# screens/settings.py
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QSlider,
    QComboBox,
    QFrame,
    QMessageBox,
    QScrollArea,
)
from PySide6.QtGui import QColor, QPalette, QIcon

from components.btn_dropshadow import add_drop_shadow
from themes.colors import *
from themes.fonts import BODY_FONT
from session import AppSession
from Database.connection import get_db_connection

IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")
SETTINGS_FILE = os.path.join(ROOT_DIR, "data", "user_settings.json")


class Settings(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setStyleSheet(f"background-color: {LIGHT};")
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        # Header Navigation
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; background-color: none; border-radius: 6px;")
        back_btn.clicked.connect(lambda: self.router.navigate("home"))
        top_layout.addWidget(back_btn)

        title = QLabel("Settings")
        title.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 700; font-size: 26px;"
        )
        top_layout.addWidget(title)

        # ---------------- Account Info Section ----------------
        main_layout.addWidget(self.make_section_label("Account Info"))

        self.username = self.make_line_edit("Enter your name")
        main_layout.addWidget(self.make_field_row("Name", self.username))

        self.email = self.make_line_edit("name@gmail.com")
        self.email.setReadOnly(True)
        main_layout.addWidget(self.make_field_row("Email", self.email))

        main_layout.addWidget(self.make_divider())

        # ---------------- Audio Section ----------------
        main_layout.addWidget(self.make_section_label("Audio"))

        self.music_slider = self.make_slider(default=70)
        main_layout.addWidget(self.make_field_row("Music", self.music_slider))

        self.sfx_slider = self.make_slider(default=70)
        main_layout.addWidget(self.make_field_row("SFX", self.sfx_slider))

        main_layout.addWidget(self.make_divider())

        # ---------------- Video Section ----------------
        main_layout.addWidget(self.make_section_label("Video"))

        self.display_mode = self.make_combo_box(["Fullscreen", "Windowed", "Borderless"])
        main_layout.addWidget(self.make_field_row("Display Mode", self.display_mode))

        self.resolution = self.make_combo_box(
            ["1920 x 1080", "1600 x 900", "1366 x 768", "1280 x 720"]
        )
        main_layout.addWidget(self.make_field_row("Resolution", self.resolution))

        self.display_mode.currentTextChanged.connect(self.on_display_mode_changed)

        main_layout.addSpacing(15)

        # ---------------- Action Buttons (Save & Logout) ----------------
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setFixedSize(200, 50)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 17px;
                font-weight: 700;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.save_btn.clicked.connect(self.save_settings)
        add_drop_shadow(self.save_btn)
        btn_layout.addWidget(self.save_btn)

        self.logout_btn = QPushButton("Log Out")
        self.logout_btn.setFixedSize(200, 50)
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #7A6B5D;
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 17px;
                font-weight: 700;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {CORAL_RED};
            }}
        """)
        self.logout_btn.clicked.connect(self.handle_logout)
        add_drop_shadow(self.logout_btn)
        btn_layout.addWidget(self.logout_btn)

        main_layout.addLayout(btn_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_current_teacher_info()
        self.load_saved_preferences()

    def on_display_mode_changed(self, mode_text):
        is_windowed = (mode_text == "Windowed")
        self.resolution.setEnabled(is_windowed)

    def load_current_teacher_info(self):
        teacher_id = AppSession.get_teacher_id()
        teacher_name = AppSession.get_teacher_name()

        if teacher_name and teacher_name != "Walang Guro":
            self.username.setText(teacher_name)

        if teacher_id:
            try:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT email, full_name FROM teachers WHERE teacher_id = ?", (teacher_id,))
                    row = cursor.fetchone()
                    if row:
                        if row['email']:
                            self.email.setText(row['email'])
                        if row['full_name']:
                            self.username.setText(row['full_name'])
            except Exception as e:
                print(f"--> Error loading teacher details: {e}")

    # ---------------- Reusable UI builders ----------------

    def make_section_label(self, text):
        label = QLabel(text)
        label.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CORAL_RED}; font-weight: 700; font-size: 18px;"
        )
        return label

    def make_field_row(self, label_text, widget):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(20)

        label = QLabel(label_text)
        label.setFixedWidth(160)
        label.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 500; font-size: 16px;"
        )
        row_layout.addWidget(label)
        row_layout.addWidget(widget, stretch=1)
        return row

    def make_line_edit(self, placeholder):
        field = QLineEdit()
        field.setFixedHeight(46)
        field.setPlaceholderText(placeholder)
        field.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        palette = field.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        field.setPalette(palette)

        field.setStyleSheet(f"""
            QLineEdit {{
                font-family: {BODY_FONT};
                font-size: 16px;
                color: {CHOCO_BROWN};
                border: 2px solid {CORAL_RED};
                border-radius: 6px;
                background-color: {LIGHT};
                padding: 8px 14px;
            }}
            QLineEdit:read-only {{
                background-color: #EFE8DA;
            }}
        """)
        return field

    def make_slider(self, default=50):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(default)
        slider.setCursor(Qt.CursorShape.PointingHandCursor)
        slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 6px;
                background: {CORAL_RED};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {CHOCO_BROWN};
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
        """)
        return slider

    def make_combo_box(self, options):
        combo = QComboBox()
        combo.addItems(options)
        combo.setFixedHeight(46)
        combo.setCursor(Qt.CursorShape.PointingHandCursor)
        combo.setStyleSheet(f"""
            QComboBox {{
                font-family: {BODY_FONT};
                font-size: 16px;
                color: {CHOCO_BROWN};
                border: 2px solid {CORAL_RED};
                border-radius: 6px;
                background-color: {LIGHT};
                padding: 8px 14px;
            }}
            QComboBox:disabled {{
                background-color: #EFE8DA;
                color: #A09488;
                border: 2px solid #D1C7B7;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                font-family: {BODY_FONT};
                font-size: 15px;
                color: {CHOCO_BROWN};
                background-color: #FFFBF0;
                selection-background-color: {CORAL_RED};
                selection-color: {LIGHT};
                border: 2px solid {CORAL_RED};
                border-radius: 4px;
                outline: none;
                padding: 4px;
            }}
            QComboBox QAbstractItemView::item {{
                min-height: 38px;
                padding-left: 10px;
                color: {CHOCO_BROWN};
                background-color: #FFFBF0;
            }}
            QComboBox QAbstractItemView::item:hover,
            QComboBox QAbstractItemView::item:selected {{
                background-color: {CORAL_RED};
                color: {LIGHT};
            }}
        """)
        return combo

    def make_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background-color: {CORAL_RED};")
        line.setFixedHeight(2)
        return line

    # ---------------- Logic ----------------

    def apply_window_settings(self, display_mode_str, res_str):
        main_win = self.window()
        if not main_win:
            return

        main_win.setWindowFlags(Qt.WindowType.Window)

        if display_mode_str == "Fullscreen":
            main_win.showFullScreen()
        elif display_mode_str == "Borderless":
            main_win.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            main_win.showMaximized()
        elif display_mode_str == "Windowed":
            main_win.showNormal()
            if "x" in res_str:
                try:
                    w, h = map(int, res_str.split("x"))
                    main_win.resize(w, h)
                    screen_geo = main_win.screen().geometry()
                    x = (screen_geo.width() - w) // 2
                    y = (screen_geo.height() - h) // 2
                    main_win.move(max(0, x), max(0, y))
                except ValueError:
                    pass

        main_win.show()

    def save_settings(self):
        mode = self.display_mode.currentText()
        res = self.resolution.currentText()
        new_name = self.username.text().strip()

        # Update teacher name in the database and session
        teacher_id = AppSession.get_teacher_id()
        if teacher_id and new_name:
            try:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE teachers SET full_name = ? WHERE teacher_id = ?", (new_name, teacher_id))
                    conn.commit()
                if hasattr(AppSession, 'set_teacher_name'):
                    AppSession.set_teacher_name(new_name)
                print(f"--> Teacher name updated to: {new_name}")
            except Exception as e:
                print(f"--> Failed to update teacher name in database: {e}")

        settings_data = {
            "music_volume": self.music_slider.value(),
            "sfx_volume": self.sfx_slider.value(),
            "display_mode": mode,
            "resolution": res,
        }

        self.apply_window_settings(mode, res)

        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings_data, f, indent=4)
            print("--> User settings saved to JSON file successfully.")

            self.show_info_dialog("Tagumpay", "Na-i-save nang matagumpay ang iyong mga setting at pangalan!")
        except Exception as e:
            print(f"--> Failed to save settings file: {e}")

    def load_saved_preferences(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "music_volume" in data:
                        self.music_slider.setValue(data["music_volume"])
                    if "sfx_volume" in data:
                        self.sfx_slider.setValue(data["sfx_volume"])
                    if "display_mode" in data:
                        self.display_mode.setCurrentText(data["display_mode"])
                    if "resolution" in data:
                        self.resolution.setCurrentText(data["resolution"])

                    self.on_display_mode_changed(self.display_mode.currentText())
            except Exception as e:
                print(f"--> Failed to load user preferences: {e}")

    def show_info_dialog(self, title_text, message_text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title_text)
        msg.setText(message_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {LIGHT};
            }}
            QMessageBox QLabel {{
                font-family: {BODY_FONT};
                font-size: 15px;
                color: {CHOCO_BROWN};
            }}
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 14px;
                font-weight: 700;
                border-radius: 6px;
                min-width: 80px;
                min-height: 32px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        msg.exec()

    def handle_logout(self):
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Kumpirmasyon")
        confirm.setText("Sigurado ka bang nais mong lumabas sa account?")
        confirm.setIcon(QMessageBox.Icon.Question)
        yes_btn = confirm.addButton("Oo", QMessageBox.ButtonRole.YesRole)
        no_btn = confirm.addButton("Hindi", QMessageBox.ButtonRole.NoRole)
        confirm.setDefaultButton(no_btn)

        confirm.setStyleSheet(f"""
            QMessageBox {{
                background-color: {LIGHT};
            }}
            QMessageBox QLabel {{
                font-family: {BODY_FONT};
                font-size: 15px;
                color: {CHOCO_BROWN};
            }}
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 14px;
                font-weight: 700;
                border-radius: 6px;
                min-width: 80px;
                min-height: 32px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        confirm.exec()

        if confirm.clickedButton() == yes_btn:
            AppSession.clear_all()
            print("--> Teacher logged out successfully. Session file removed.")
            self.router.navigate("createacc")