import os
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
)
from PySide6.QtGui import QColor, QPalette, QIcon

from components.btn_dropshadow import add_drop_shadow
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


class Settings(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("home"))
        top_layout.addWidget(back_btn)

        title = QLabel("Settings")
        title.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 700; font-size: 26px;"
        )
        top_layout.addWidget(title)

        # ---------------- Account Info Section ----------------
        main_layout.addWidget(self.make_section_label("Account Info"))

        self.username = self.make_line_edit("Enter your username")
        main_layout.addWidget(self.make_field_row("Username", self.username))

        self.email = self.make_line_edit("name@gmail.com")
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

        main_layout.addSpacing(10)

        # ---------------- Save Button ----------------
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setFixedSize(220, 52)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 18px;
                font-weight: 700;
                padding: 2px 6px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.save_btn.clicked.connect(self.save_settings)
        add_drop_shadow(self.save_btn)

        main_layout.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignCenter)

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
            QComboBox::drop-down {{
                border: none;
                width: 30px;
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

    def save_settings(self):
        settings_data = {
            "username": self.username.text().strip(),
            "email": self.email.text().strip(),
            "music_volume": self.music_slider.value(),
            "sfx_volume": self.sfx_slider.value(),
            "display_mode": self.display_mode.currentText(),
            "resolution": self.resolution.currentText(),
        }
        print("--> Settings saved:", settings_data)
        # TODO: persist settings_data (e.g. write to a config file or app state)