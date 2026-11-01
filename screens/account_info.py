# screens/account_info.py

import os
import re
import sys
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from local .env file
load_dotenv()

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
    QToolButton,
    QMessageBox,
    QScrollArea
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
        self.generated_code = None  # Stores the random verification code temporarily
        self.code_timestamp = 0     # Stores when the code was generated for expiration tracking

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Wrap in ScrollArea to fully support 1366x768 and lower laptop resolutions without clipping
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setStyleSheet(f"background-color: {LIGHT};")
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(12)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        # Logo
        logo = QLabel()
        logo.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "logoo.png")).scaled(
                220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        main_layout.addWidget(logo)

        # Form Inputs Layout
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.setSpacing(10)
        main_layout.addLayout(input_layout)

        # --- Full Name Field Group ---
        name_group = QVBoxLayout()
        name_group.setSpacing(4)
        name_group.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel("Full Name")
        name_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 14px; color: {CORAL_RED}; font-weight: 600;"
        )
        name_group.addWidget(name_label)

        self.full_name = QLineEdit()
        self.full_name.setFixedSize(888, 44)
        self.full_name.setPlaceholderText("e.g. Teacher Maria Santos")
        self.set_normal_style(self.full_name)
        name_group.addWidget(self.full_name)

        self.name_error = QLabel("")
        self.name_error.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 12px; color: #d93025; font-weight: 600;")
        self.name_error.hide()
        name_group.addWidget(self.name_error)

        input_layout.addLayout(name_group)

        # --- Email Field Group ---
        email_group = QVBoxLayout()
        email_group.setSpacing(4)
        email_group.setContentsMargins(0, 0, 0, 0)

        email_label = QLabel("Email")
        email_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 14px; color: {CORAL_RED}; font-weight: 600;"
        )
        email_group.addWidget(email_label)

        email_row_layout = QHBoxLayout()
        email_row_layout.setSpacing(10)
        email_row_layout.setContentsMargins(0, 0, 0, 0)

        self.email = QLineEdit()
        self.email.setFixedSize(720, 44)
        self.email.setPlaceholderText("name@gmail.com")
        self.set_normal_style(self.email)

        palette = self.email.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        self.email.setPalette(palette)
        email_row_layout.addWidget(self.email)

        self.send_code_btn = QPushButton("Send Code")
        self.send_code_btn.setFixedSize(158, 44)
        self.send_code_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_code_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 15px;
                font-weight: 700;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.send_code_btn.clicked.connect(self.send_verification_email)
        email_row_layout.addWidget(self.send_code_btn)

        email_container = QWidget()
        email_container.setFixedWidth(888)
        email_container.setLayout(email_row_layout)
        email_group.addWidget(email_container)

        self.email_error = QLabel("")
        self.email_error.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 12px; color: #d93025; font-weight: 600;")
        self.email_error.hide()
        email_group.addWidget(self.email_error)

        input_layout.addLayout(email_group)

        # --- Verification Code Field Group ---
        code_group = QVBoxLayout()
        code_group.setSpacing(4)
        code_group.setContentsMargins(0, 0, 0, 0)

        code_label = QLabel("Verification Code")
        code_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 14px; color: {CORAL_RED}; font-weight: 600;"
        )
        code_group.addWidget(code_label)

        self.code_input = QLineEdit()
        self.code_input.setFixedSize(888, 44)
        self.code_input.setPlaceholderText("Enter 6-digit verification code")
        self.set_normal_style(self.code_input)
        code_group.addWidget(self.code_input)

        self.code_error = QLabel("")
        self.code_error.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 12px; color: #d93025; font-weight: 600;")
        self.code_error.hide()
        code_group.addWidget(self.code_error)

        input_layout.addLayout(code_group)

        # --- Password Field Group ---
        pass_group = QVBoxLayout()
        pass_group.setSpacing(4)
        pass_group.setContentsMargins(0, 0, 0, 0)

        pass_label = QLabel("Password")
        pass_label.setStyleSheet(
            f"font-family: {BODY_FONT}; font-size: 14px; color: {CORAL_RED}; font-weight: 600;"
        )
        pass_group.addWidget(pass_label)

        self.password = QLineEdit()
        self.password.setFixedSize(888, 44)
        self.password.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.password.setPlaceholderText("e.g. password123")
        self.password.setEchoMode(QLineEdit.Password)
        self.set_normal_style(self.password)

        palette = self.password.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        self.password.setPalette(palette)
        pass_group.addWidget(self.password)

        self.password_error = QLabel("")
        self.password_error.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 12px; color: #d93025; font-weight: 600;")
        self.password_error.hide()
        pass_group.addWidget(self.password_error)

        input_layout.addLayout(pass_group)

        self.ICON_PIXEL_SIZE = 28
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

        # Return Navigation Row
        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header_row.setContentsMargins(0, 2, 0, 2)
        
        create_label = QLabel("Nais mo bang bumalik?")
        create_label.setStyleSheet(
            f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 600; font-size: 14px;"
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
                font-size: 14px;
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
        
        header_container = QWidget()
        header_container.setFixedWidth(888)
        header_container.setLayout(header_row)
        input_layout.addWidget(header_container, alignment=Qt.AlignmentFlag.AlignLeft)

        # Create Account Button
        self.create_btn = QPushButton("Create account")
        self.create_btn.setFixedSize(300, 48)
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 18px;
                font-weight: 900;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)

        self.create_btn.clicked.connect(self.validate_and_create_account)
        add_drop_shadow(self.create_btn)

        input_layout.addWidget(
            self.create_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Clear errors when typing
        self.full_name.textChanged.connect(lambda: (self.name_error.hide(), self.set_normal_style(self.full_name)))
        self.email.textChanged.connect(self.clear_email_error)
        self.code_input.textChanged.connect(lambda: (self.code_error.hide(), self.set_normal_style(self.code_input)))
        self.password.textChanged.connect(self.clear_password_error)

        # Bottom Graphic Images
        image_bottom = QHBoxLayout()
        image_bottom.setSpacing(0)
        image_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_bottom.setContentsMargins(0, 10, 0, 0)

        for img_name in ["kids2.png", "kids1.png", "kids2.png", "kids1.png"]:
            kid = QLabel()
            kid.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            kid.setPixmap(
                QPixmap(os.path.join(IMAGE_DIR, img_name)).scaled(
                    160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
            kid.setAlignment(Qt.AlignmentFlag.AlignLeft)
            image_bottom.addWidget(kid)

        main_layout.addLayout(image_bottom)

    def showEvent(self, event):
        """Automatically clears input fields, codes, and errors whenever the registration screen is shown."""
        super().showEvent(event)
        self.full_name.clear()
        self.email.clear()
        self.code_input.clear()
        self.password.clear()
        self.generated_code = None
        self.code_timestamp = 0
        self.name_error.hide()
        self.email_error.hide()
        self.code_error.hide()
        self.password_error.hide()
        self.reset_styles()

    def set_normal_style(self, widget):
        widget.setStyleSheet(f"""
            QLineEdit {{
                font-family: {BODY_FONT};
                font-size: 15px;
                color: {CHOCO_BROWN};
                border: 2px solid {CORAL_RED};        
                border-radius: 6px;
                background-color: {LIGHT}; 
                padding: 4px 12px;        
            }}
        """)

    def set_error_style(self, widget):
        widget.setStyleSheet(f"""
            QLineEdit {{
                font-family: {BODY_FONT};
                font-size: 15px;
                color: {CHOCO_BROWN};
                border: 2px solid #d93025;        
                border-radius: 6px;
                background-color: {LIGHT}; 
                padding: 4px 12px;        
            }}
        """)

    def reset_styles(self):
        self.set_normal_style(self.full_name)
        self.set_normal_style(self.email)
        self.set_normal_style(self.code_input)
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

    def send_verification_email(self):
        email_text = self.email.text().strip()
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not email_text or not re.match(email_pattern, email_text):
            self.email_error.setText("✖  Please enter a valid email address first.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            return

        # Disable button and show loading state
        self.send_code_btn.setEnabled(False)
        self.send_code_btn.setText("Sending...")
        self.send_code_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #cccccc;
                color: {CHOCO_BROWN};
                font-family: {BODY_FONT};
                font-size: 15px;
                font-weight: 700;
                border-radius: 6px;
            }}
        """)
        self.send_code_btn.repaint()

        self.generated_code = str(random.randint(100000, 999999))
        self.code_timestamp = time.time()  # Record code creation time for expiration

        # Securely load credentials from environment variables (.env)
        sender_email = os.getenv("SENDER_EMAIL")
        app_password = os.getenv("GMAIL_APP_PASSWORD")

        if not sender_email or not app_password:
            print("--> Error: SENDER_EMAIL or GMAIL_APP_PASSWORD not found in environment variables.")
            self.email_error.setText("✖ Configuration error: Missing email credentials.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            self.reset_send_button()
            return

        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email_text
            msg["Subject"] = "BasaMatika Email Verification Code"

            body = f"Mabuhay! Your verification code for BasaMatika is: {self.generated_code}\n\nThis code will expire in 5 minutes."
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, email_text, msg.as_string())
            server.quit()

            print(f"--> Verification code sent successfully to {email_text}")

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Verification Code Sent")
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText(f"A 6-digit verification code has been successfully emailed to:\n<b>{email_text}</b>")
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {LIGHT};
                    font-family: {BODY_FONT};
                    font-size: 16px;
                    color: {CHOCO_BROWN};
                }}
                QLabel {{
                    color: {CHOCO_BROWN};
                    font-size: 15px;
                }}
                QPushButton {{
                    background-color: {CORAL_RED};
                    color: {LIGHT};
                    font-family: {BODY_FONT};
                    font-size: 14px;
                    font-weight: 700;
                    padding: 6px 16px;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: #d94338;
                }}
            """)
            msg_box.exec()

        except Exception as e:
            print(f"--> Failed to send verification email: {e}")
            self.email_error.setText(f"✖ Failed to send email. Check network connection.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            self.generated_code = None
            self.code_timestamp = 0

        # Restore send button state
        self.reset_send_button()

    def reset_send_button(self):
        """Restores the Send Code button back to normal style and functionality."""
        self.send_code_btn.setEnabled(True)
        self.send_code_btn.setText("Send Code")
        self.send_code_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 15px;
                font-weight: 700;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)

    def validate_and_create_account(self):
        print("--> BUTTON CLICKED! Validating inputs...")

        name_text = self.full_name.text().strip()
        email_text = self.email.text().strip()
        code_text = self.code_input.text().strip()
        password_text = self.password.text().strip()

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        has_error = False

        self.name_error.hide()
        self.email_error.hide()
        self.code_error.hide()
        self.password_error.hide()
        self.reset_styles()

        if not name_text:
            self.name_error.setText("✖  Please enter your full name.")
            self.name_error.setVisible(True)
            self.set_error_style(self.full_name)
            has_error = True

        if not email_text or not re.match(email_pattern, email_text):
            self.email_error.setText("✖  Please enter a valid email address.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            has_error = True

        # Check code validity and 5-minute (300 seconds) expiration limit
        if not code_text or code_text != self.generated_code:
            self.code_error.setText("✖  Invalid verification code. Please check your email.")
            self.code_error.setVisible(True)
            self.set_error_style(self.code_input)
            has_error = True
        elif self.code_timestamp and (time.time() - self.code_timestamp > 300):
            self.code_error.setText("✖  Verification code has expired. Please request a new one.")
            self.code_error.setVisible(True)
            self.set_error_style(self.code_input)
            has_error = True

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
            print("--> Validation failed! Check fields and verification code.")
            return

        print("--> Validation passed! Saving account to local database...")

        try:
            teacher_id = create_teacher_account(
                full_name=name_text,  
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