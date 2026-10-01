# screens/account_info.py

import os
import re
import sys

# Ensure root folder (CapstoneProject2) is in the Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QToolButton
)
from PySide6.QtGui import QPixmap, QColor, QPalette, QIcon

from components.btn_dropshadow import add_drop_shadow
from themes.colors import *
from themes.fonts import BODY_FONT

# DATABASE & SESSION IMPORTS 
from Database.queries import create_teacher_account
from session import AppSession

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image")
ICON_DIR = os.path.join(BASE_DIR, "assets", "icons")


def make_eye_icon(filename, size=36):
    """Load an icon from ICON_DIR and scale it to the given pixel size."""
    pixmap = QPixmap(os.path.join(ICON_DIR, filename)).scaled(
        size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
    )
    return QIcon(pixmap)


class AccountInfo(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo = QLabel()
        logo.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(
            QPixmap(
                QPixmap(os.path.join(IMAGE_DIR, "logoo.png")).scaled(
                    350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        )
        main_layout.addWidget(logo)

        # Form Inputs Layout
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.setSpacing(4)
        main_layout.addLayout(input_layout)

        # Switch prompt header (Go back to Create Account splash)
        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        create_label = QLabel("Nais mo bang bumalik?")
        create_label.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 600; font-size: 16px;"
        )
        header_row.addWidget(create_label)

        switch_btn = QPushButton("Bumalik")
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
        # Route back to create account splash screen
        switch_btn.clicked.connect(lambda: self.router.navigate("createacc"))
        header_row.addWidget(switch_btn)
        header_row.addStretch()
        
        header_container = QWidget()
        header_container.setFixedWidth(888)
        header_container.setLayout(header_row)
        input_layout.addWidget(header_container, alignment=Qt.AlignmentFlag.AlignLeft)

        input_layout.addSpacing(6)

        # Email Field
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

        # Password Field 
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

        # Set initial style
        self.reset_styles()

        # Create Account Button
        self.create_btn = QPushButton("Create account")
        self.create_btn.setFixedSize(340, 56)
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.setStyleSheet(f"""
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

        # Connect click event BEFORE drop shadow
        self.create_btn.clicked.connect(self.validate_and_create_account)

        # Add shadow after setting up signal
        add_drop_shadow(self.create_btn)

        # Clear errors when typing
        self.email.textChanged.connect(self.clear_email_error)
        self.password.textChanged.connect(self.clear_password_error)

        input_layout.addSpacing(10)
        input_layout.addWidget(
            self.create_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Bottom Graphic Images
        image_bottom = QHBoxLayout()
        image_bottom.setSpacing(0)
        image_bottom.setAlignment(Qt.AlignCenter)
        image_bottom.setContentsMargins(0, 5, 0, 0)

        for img_name in ["kids2.png", "kids1.png", "kids2.png", "kids1.png"]:
            kid = QLabel()
            kid.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            kid.setPixmap(
                QPixmap(
                    QPixmap(os.path.join(IMAGE_DIR, img_name)).scaled(
                        320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                )
            )
            kid.setAlignment(Qt.AlignmentFlag.AlignLeft)
            image_bottom.addWidget(kid)

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

    def validate_and_create_account(self):
        print("--> BUTTON CLICKED! Validating inputs...")

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
            self.email_error.setText("✖  Hmm... that doesn't look like a valid email address.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            has_error = True

        # Password Validation
        if not password_text:
            self.password_error.setText("✖  Please enter a password.")
            self.password_error.setVisible(True)
            self.set_error_style(self.password)
            has_error = True
        elif len(password_text) < 8:
            self.password_error.setText("✖  Password must be at least 8 characters long.")
            self.password_error.setVisible(True)
            self.set_error_style(self.password)
            has_error = True

        if has_error:
            print("--> Validation failed! Showing inline errors.")
            return

        print("--> Validation passed! Saving account to local database...")

        # LOCAL DATABASE & SESSION INTEGRATION 
        try:
            teacher_id = create_teacher_account(
                full_name="Guro",  
                email=email_text,
                raw_password=password_text,
                section_name="Kindergarten - Paharang"
            )

            AppSession.set_teacher(teacher_id, email_text)
            print(f"--> Account created! Teacher ID: {teacher_id}")
            self.router.navigate("home")

        except Exception as e:
            print(f"--> Failed to create account in database: {e}")
            self.email_error.setText("✖  This email is already registered.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)