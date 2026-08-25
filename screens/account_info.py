import os
import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PySide6.QtGui import QPixmap, QColor, QPalette

from components.btn_dropshadow import add_drop_shadow
from themes.colors import *
from themes.fonts import BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")


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
                    400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        )
        main_layout.addWidget(logo)

        # Form Inputs Layout
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.setSpacing(4)
        main_layout.addLayout(input_layout)

        create = QLabel("Create an account")
        create.setAlignment(Qt.AlignmentFlag.AlignLeft)
        create.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 600; font-size: 18px;"
        )
        input_layout.addWidget(create)

        # --- Email Field ---
        email_label = QLabel("Email")
        email_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;"
        )
        email_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_layout.addWidget(email_label)

        self.email = QLineEdit()
        self.email.setFixedSize(888, 56)
        self.email.setPlaceholderText("name@gmail.com")
        self.email.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        palette = self.email.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        self.email.setPalette(palette)

        input_layout.addWidget(self.email)

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
        input_layout.addWidget(self.email_error)

        input_layout.addSpacing(6)

        # --- Password Field ---
        pass_label = QLabel("Password")
        pass_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;"
        )
        pass_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_layout.addWidget(pass_label)

        self.password = QLineEdit()
        self.password.setFixedSize(888, 56)
        self.password.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.password.setPlaceholderText("********")
        self.password.setEchoMode(QLineEdit.Password)

        palette = self.password.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        self.password.setPalette(palette)

        input_layout.addWidget(self.password)

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
        input_layout.addWidget(self.password_error)

        input_layout.addSpacing(10)

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

        main_layout.addWidget(
            self.create_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Bottom Graphic Images
        image_bottom = QHBoxLayout()
        image_bottom.setSpacing(0)
        image_bottom.setAlignment(Qt.AlignCenter)
        image_bottom.setContentsMargins(0, 5, 0, 0)

        #horizontal image of kids
        kids1 = QLabel()
        kids1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        kids1.setPixmap(
            QPixmap(
                QPixmap(os.path.join(IMAGE_DIR, "kids2.png")).scaled(
                    320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        )
        kids1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        image_bottom.addWidget(kids1)

        kids2 = QLabel()
        kids2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        kids2.setPixmap(
            QPixmap(
                QPixmap(os.path.join(IMAGE_DIR, "kids1.png")).scaled(
                    320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        )
        kids2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        image_bottom.addWidget(kids2)

        kids3 = QLabel()
        kids3.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        kids3.setPixmap(
            QPixmap(
                QPixmap(os.path.join(IMAGE_DIR, "kids2.png")).scaled(
                    320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        )
        kids3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        image_bottom.addWidget(kids3)

        kids4 = QLabel()
        kids4.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        kids4.setPixmap(
            QPixmap(
                QPixmap(os.path.join(IMAGE_DIR, "kids1.png")).scaled(
                    320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        )
        kids4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        image_bottom.addWidget(kids4)

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
                padding: 10px 16px;        
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
                padding: 10px 16px;        
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

    def validate_and_create_account(self):
        print("--> BUTTON CLICKED! Validating inputs...")  # Debug print in terminal

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

        print("--> Validation passed! Navigating to home...")
        self.router.navigate("home")