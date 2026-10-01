import os
import re
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
    QToolButton,
    QMessageBox,
    QScrollArea
)
from PySide6.QtGui import QPixmap, QColor, QPalette, QIcon

from components.btn_dropshadow import add_drop_shadow
from themes.colors import *
from themes.fonts import BODY_FONT
from session import AppSession
from Database.connection import get_db_connection

IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICON_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


def make_eye_icon(filename, size=36):
    """Load an icon from ICON_DIR and scale it to the given pixel size."""
    icon_path = os.path.join(ICON_DIR, filename)
    if os.path.exists(icon_path):
        pixmap = QPixmap(icon_path).scaled(
            size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        return QIcon(pixmap)
    return QIcon()


class Login(QWidget):
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
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        # Logo
        logo = QLabel()
        logo.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "logoo.png")).scaled(
                260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        main_layout.addWidget(logo)

        # Form Inputs Layout
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.setSpacing(4)
        main_layout.addLayout(input_layout)

        # Switch prompt header
        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        create_label = QLabel("Wala pang account?")
        create_label.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 600; font-size: 16px;"
        )
        header_row.addWidget(create_label)

        switch_btn = QPushButton("Gumawa ng isa")
        switch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        switch_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                font-family: {BODY_FONT};
                color: {CORAL_RED};
                font-weight: 700;
                font-size: 16px;
                text-align: left;
            }}
            QPushButton:hover {{
                color: #d94338;
                text-decoration: underline;
            }}
        """)
        switch_btn.clicked.connect(lambda: self.router.navigate("createacc"))
        header_row.addWidget(switch_btn)
        header_row.addStretch()
        
        # Wrap header row in a container with fixed width matching inputs
        header_container = QWidget()
        header_container.setFixedWidth(888)
        header_container.setLayout(header_row)
        input_layout.addWidget(header_container, alignment=Qt.AlignmentFlag.AlignLeft)

        input_layout.addSpacing(6)

        # --- Email Field ---
        email_label = QLabel("Email")
        email_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;"
        )
        email_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_layout.addWidget(email_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.email = QLineEdit()
        self.email.setFixedSize(888, 56)
        self.email.setPlaceholderText("name@gmail.com")
        self.email.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        palette = self.email.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        self.email.setPalette(palette)
        input_layout.addWidget(self.email, alignment=Qt.AlignmentFlag.AlignLeft)

        # Email Inline Error Label
        self.email_error = QLabel("")
        self.email_error.setFixedWidth(888)
        self.email_error.setStyleSheet(f"""
            font-family: {BODY_FONT};
            font-size: 14px;
            color: #d93025;
            font-weight: 600;
            padding-top: 2px;
        """)
        self.email_error.hide()
        input_layout.addWidget(self.email_error, alignment=Qt.AlignmentFlag.AlignLeft)

        input_layout.addSpacing(6)

        # --- Password Field ---
        pass_label = QLabel("Password")
        pass_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;"
        )
        pass_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_layout.addWidget(pass_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.password = QLineEdit()
        self.password.setFixedSize(888, 56)
        self.password.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.password.setPlaceholderText("eg. 123abcd")
        self.password.setEchoMode(QLineEdit.Password)

        palette = self.password.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        self.password.setPalette(palette)
        input_layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignLeft)

        # Password Inline Error Label
        self.password_error = QLabel("")
        self.password_error.setFixedWidth(888)
        self.password_error.setStyleSheet(f"""
            font-family: {BODY_FONT};
            font-size: 14px;
            color: #d93025;
            font-weight: 600;
            padding-top: 2px;
        """)
        self.password_error.hide()
        input_layout.addWidget(self.password_error, alignment=Qt.AlignmentFlag.AlignLeft)

        self.ICON_PIXEL_SIZE = 36

        self.eye_btn = QToolButton(self.password)
        self.eye_btn.setCheckable(True)
        self.eye_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_btn.setStyleSheet("background: transparent; border: none;")
        self.eye_btn.setIcon(make_eye_icon("close_eye.png", self.ICON_PIXEL_SIZE))
        self.eye_btn.setIconSize(QSize(self.ICON_PIXEL_SIZE, self.ICON_PIXEL_SIZE))
        self.eye_btn.toggled.connect(self.toggle_password_visibility)
        
        pass_layout = QHBoxLayout(self.password)
        pass_layout.setContentsMargins(0, 0, 10, 0)
        pass_layout.addStretch()
        pass_layout.addWidget(self.eye_btn)

        self.reset_styles()

        # Log-in Button
        self.login_btn = QPushButton("Log-in")
        self.login_btn.setFixedSize(340, 56)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 22px;
                font-weight: 900;
                padding: 2px 6px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.login_btn.clicked.connect(self.handle_login_action)
        add_drop_shadow(self.login_btn)

        # Clear errors when typing
        self.email.textChanged.connect(self.clear_email_error)
        self.password.textChanged.connect(self.clear_password_error)

        input_layout.addSpacing(10)
        input_layout.addWidget(
            self.login_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Bottom Graphic Images
        image_bottom = QHBoxLayout()
        image_bottom.setSpacing(0)
        image_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_bottom.setContentsMargins(0, 10, 0, 0)

        for img_name in ["kids2.png", "kids1.png", "kids2.png", "kids1.png"]:
            kid_label = QLabel()
            kid_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            kid_path = os.path.join(IMAGE_DIR, img_name)
            if os.path.exists(kid_path):
                kid_label.setPixmap(
                    QPixmap(kid_path).scaled(
                        220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                )
            kid_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            image_bottom.addWidget(kid_label)

        main_layout.addLayout(image_bottom)

    def set_normal_style(self, widget):
        widget.setStyleSheet(f"""
            QLineEdit {{
                font-family: {BODY_FONT};
                font-size: 18px;
                color: {CHOCO_BROWN};
                border: 2px solid {CORAL_RED};        
                border-radius: 6px;
                background-color: {LIGHT}; 
                padding: 10px 50px 10px 16px;        
            }}
        """)

    def set_error_style(self, widget):
        widget.setStyleSheet(f"""
            QLineEdit {{
                font-family: {BODY_FONT};
                font-size: 18px;
                color: {CHOCO_BROWN};
                border: 2px solid #d93025;        
                border-radius: 6px;
                background-color: {LIGHT}; 
                padding: 10px 50px 10px 16px;        
            }}
        """)

    def reset_styles(self):
        self.set_normal_style(self.email)
        self.set_normal_style(self.password)

    def clear_email_error(self):
        self.email_error.hide()
        self.set_normal_style(self.email)

    def clear_password_error(self):
        self.password_error.hide()
        self.set_normal_style(self.password)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password.setEchoMode(QLineEdit.Normal)
            self.eye_btn.setIcon(make_eye_icon("eye_open.png", self.ICON_PIXEL_SIZE))
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.eye_btn.setIcon(make_eye_icon("close_eye.png", self.ICON_PIXEL_SIZE))

    def handle_login_action(self):
        email_text = self.email.text().strip()
        password_text = self.password.text().strip()

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        has_error = False

        self.email_error.hide()
        self.password_error.hide()
        self.reset_styles()

        # Email Validation
        if not email_text:
            self.email_error.setText("✖  Please enter your email address.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            has_error = True
        elif not re.match(email_pattern, email_text):
            self.email_error.setText("✖  Invalid email address format.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            has_error = True

        # Password Validation
        if not password_text:
            self.password_error.setText("✖  Please enter your password.")
            self.password_error.setVisible(True)
            self.set_error_style(self.password)
            has_error = True

        if has_error:
            return

        # Query Database for Authentication
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # FIXED: Changed 'name' to 'full_name' to match the database column schema
                cursor.execute(
                    "SELECT teacher_id, full_name, email FROM teachers WHERE email = ?",
                    (email_text,)
                )
                teacher = cursor.fetchone()

                if teacher:
                    teacher_id = teacher["teacher_id"]
                    teacher_name = teacher["full_name"]  # FIXED: Access 'full_name'

                    # Save session persistently
                    AppSession.set_teacher(teacher_id=teacher_id, full_name=teacher_name, remember=True)
                    print(f"--> Successful login for: {teacher_name}")

                    # Navigate to home
                    self.router.navigate("home")
                else:
                    self.email_error.setText("✖  No registered account found for this email.")
                    self.email_error.setVisible(True)
                    self.set_error_style(self.email)
        except Exception as e:
            print(f"--> Database login error: {e}")
            self.show_error_dialog("Error", f"An issue occurred with the database: {e}")

    def show_error_dialog(self, title_text, message_text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title_text)
        msg.setText(message_text)
        msg.setIcon(QMessageBox.Icon.Warning)
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