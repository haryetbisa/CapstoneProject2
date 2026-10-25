# screens/forgot_pass.py

import os
import re
import sys
import random
import smtplib
import bcrypt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
from Database.connection import get_db_connection

IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICON_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


def make_eye_icon(filename, size=36):
    pixmap = QPixmap(os.path.join(ICON_DIR, filename)).scaled(
        size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
    )
    return QIcon(pixmap)


class ForgotPassword(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.generated_code = None
        self.verified_email = None

        # Outer layout with ScrollArea for screen responsiveness
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

        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.setSpacing(4)
        main_layout.addLayout(input_layout)

        # --- Email Field & Send Code Button ---
        email_label = QLabel("Registered Email")
        email_label.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;")
        input_layout.addWidget(email_label, alignment=Qt.AlignmentFlag.AlignLeft)

        email_row_layout = QHBoxLayout()
        email_row_layout.setSpacing(10)
        email_row_layout.setContentsMargins(0, 0, 0, 0)

        self.email = QLineEdit()
        self.email.setFixedSize(720, 56)
        self.email.setPlaceholderText("name@gmail.com")
        self.set_normal_style(self.email)
        email_row_layout.addWidget(self.email)

        self.send_code_btn = QPushButton("Send Code")
        self.send_code_btn.setFixedSize(158, 56)
        self.send_code_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_code_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 16px;
                font-weight: 700;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.send_code_btn.clicked.connect(self.send_recovery_code)
        email_row_layout.addWidget(self.send_code_btn)

        email_container = QWidget()
        email_container.setFixedWidth(888)
        email_container.setLayout(email_row_layout)
        input_layout.addWidget(email_container, alignment=Qt.AlignmentFlag.AlignLeft)

        self.email_error = QLabel("")
        self.email_error.setFixedWidth(888)
        self.email_error.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 14px; color: #d93025; font-weight: 600;")
        self.email_error.hide()
        input_layout.addWidget(self.email_error, alignment=Qt.AlignmentFlag.AlignLeft)

        input_layout.addSpacing(6)

        # --- Verification Code Field ---
        code_label = QLabel("Verification Code")
        code_label.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;")
        input_layout.addWidget(code_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.code_input = QLineEdit()
        self.code_input.setFixedSize(888, 56)
        self.code_input.setPlaceholderText("Enter 6-digit code")
        self.set_normal_style(self.code_input)
        input_layout.addWidget(self.code_input, alignment=Qt.AlignmentFlag.AlignLeft)

        self.code_error = QLabel("")
        self.code_error.setFixedWidth(888)
        self.code_error.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 14px; color: #d93025; font-weight: 600;")
        self.code_error.hide()
        input_layout.addWidget(self.code_error, alignment=Qt.AlignmentFlag.AlignLeft)

        input_layout.addSpacing(6)

        # --- New Password Field ---
        pass_label = QLabel("New Password")
        pass_label.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;")
        input_layout.addWidget(pass_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.new_password = QLineEdit()
        self.new_password.setFixedSize(888, 56)
        self.new_password.setPlaceholderText("At least 8 characters")
        self.new_password.setEchoMode(QLineEdit.Password)
        self.set_password_style(self.new_password)  # Uses dedicated padding for the eye button!
        input_layout.addWidget(self.new_password, alignment=Qt.AlignmentFlag.AlignLeft)

        self.password_error = QLabel("")
        self.password_error.setFixedWidth(888)
        self.password_error.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 14px; color: #d93025; font-weight: 600;")
        self.password_error.hide()
        input_layout.addWidget(self.password_error, alignment=Qt.AlignmentFlag.AlignLeft)

        # Password visibility toggle button layout
        self.ICON_PIXEL_SIZE = 36
        self.eye_btn = QToolButton(self.new_password)
        self.eye_btn.setCheckable(True)
        self.eye_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_btn.setStyleSheet("background: transparent; border: none;")
        self.eye_btn.setIcon(make_eye_icon("close_eye.png", self.ICON_PIXEL_SIZE))
        self.eye_btn.setIconSize(QSize(self.ICON_PIXEL_SIZE, self.ICON_PIXEL_SIZE))
        self.eye_btn.toggled.connect(self.toggle_password_visibility)
        
        pass_layout = QHBoxLayout(self.new_password)
        pass_layout.setContentsMargins(0, 0, 10, 0)
        pass_layout.addStretch()
        pass_layout.addWidget(self.eye_btn)

        input_layout.addSpacing(10)

        # --- Back to Login Navigation Row ---
        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header_row.setContentsMargins(0, 0, 0, 0)
        
        back_label = QLabel("Naalala mo na ba?")
        back_label.setStyleSheet(f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 600; font-size: 16px;")
        header_row.addWidget(back_label)

        switch_btn = QPushButton("Mag-log in")
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
        switch_btn.clicked.connect(lambda: self.router.navigate("login"))
        header_row.addWidget(switch_btn)
        header_row.addStretch()
        
        header_container = QWidget()
        header_container.setFixedWidth(888)
        header_container.setLayout(header_row)
        input_layout.addWidget(header_container, alignment=Qt.AlignmentFlag.AlignLeft)

        input_layout.addSpacing(14)

        # --- Reset Password Button ---
        self.reset_btn = QPushButton("Reset Password")
        self.reset_btn.setFixedSize(340, 56)
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 22px;
                font-weight: 900;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        self.reset_btn.clicked.connect(self.validate_and_reset_password)
        add_drop_shadow(self.reset_btn)
        input_layout.addWidget(self.reset_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Clear errors on typing
        self.email.textChanged.connect(lambda: (self.email_error.hide(), self.set_normal_style(self.email)))
        self.code_input.textChanged.connect(lambda: (self.code_error.hide(), self.set_normal_style(self.code_input)))
        self.new_password.textChanged.connect(lambda: (self.password_error.hide(), self.set_password_style(self.new_password)))

        # Bottom Images
        image_bottom = QHBoxLayout()
        image_bottom.setSpacing(0)
        image_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_bottom.setContentsMargins(0, 10, 0, 0)
        for img_name in ["kids2.png", "kids1.png", "kids2.png", "kids1.png"]:
            kid_label = QLabel()
            kid_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            kid_path = os.path.join(IMAGE_DIR, img_name)
            if os.path.exists(kid_path):
                kid_label.setPixmap(QPixmap(kid_path).scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_bottom.addWidget(kid_label)
        main_layout.addLayout(image_bottom)

    def showEvent(self, event):
        super().showEvent(event)
        self.email.clear()
        self.code_input.clear()
        self.new_password.clear()
        self.generated_code = None
        self.verified_email = None
        self.email_error.hide()
        self.code_error.hide()
        self.password_error.hide()
        self.set_normal_style(self.email)
        self.set_normal_style(self.code_input)
        self.set_password_style(self.new_password)

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

    def set_password_style(self, widget):
        # Includes extra right padding (50px) so typed text doesn't overlap the eye icon
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
                padding: 10px 16px;        
            }}
        """)

    def toggle_password_visibility(self, checked):
        if checked:
            self.new_password.setEchoMode(QLineEdit.Normal)
            self.eye_btn.setIcon(make_eye_icon("eye_open.png", self.ICON_PIXEL_SIZE))
        else:
            self.new_password.setEchoMode(QLineEdit.Password)
            self.eye_btn.setIcon(make_eye_icon("close_eye.png", self.ICON_PIXEL_SIZE))

    def send_recovery_code(self):
        email_text = self.email.text().strip().lower()
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not email_text or not re.match(email_pattern, email_text):
            self.email_error.setText("✖  Please enter a valid email address.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT teacher_id FROM teachers WHERE email = ?", (email_text,))
                teacher = cursor.fetchone()

            if not teacher:
                self.email_error.setText("✖  No account found with this email address.")
                self.email_error.setVisible(True)
                self.set_error_style(self.email)
                return

        except Exception as e:
            print(f"--> Database check error: {e}")
            return

        self.generated_code = str(random.randint(100000, 999999))
        self.verified_email = email_text

        sender_email = "basamakita.official@gmail.com"
        app_password = "tvpq ldae oeiv mjhn"

        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email_text
            msg["Subject"] = "BasaMatika Password Reset Code"

            body = f"Mabuhay! Your password reset verification code is: {self.generated_code}"
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, email_text, msg.as_string())
            server.quit()

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Recovery Code Sent")
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText(f"A password reset code has been emailed to:\n<b>{email_text}</b>")
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {LIGHT};
                    font-family: {BODY_FONT};
                    font-size: 16px;
                    color: {CHOCO_BROWN};
                }}
                QLabel {{ color: {CHOCO_BROWN}; font-size: 15px; }}
                QPushButton {{
                    background-color: {CORAL_RED};
                    color: {LIGHT};
                    font-family: {BODY_FONT};
                    font-size: 14px;
                    font-weight: 700;
                    padding: 6px 16px;
                    border-radius: 4px;
                }}
                QPushButton:hover {{ background-color: #d94338; }}
            """)
            msg_box.exec()

        except Exception as e:
            print(f"--> Failed to send recovery email: {e}")
            self.email_error.setText("✖ Failed to send email. Check network connection.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)

    def validate_and_reset_password(self):
        email_text = self.email.text().strip().lower()
        code_text = self.code_input.text().strip()
        password_text = self.new_password.text().strip()
        has_error = False

        if not email_text or email_text != self.verified_email:
            self.email_error.setText("✖  Please verify this email first.")
            self.email_error.setVisible(True)
            self.set_error_style(self.email)
            has_error = True

        if not code_text or code_text != self.generated_code:
            self.code_error.setText("✖  Invalid or missing verification code.")
            self.code_error.setVisible(True)
            self.set_error_style(self.code_input)
            has_error = True

        if not password_text:
            self.password_error.setText("✖  Please enter a new password.")
            self.password_error.setVisible(True)
            self.set_password_style(self.new_password)
            has_error = True
        elif len(password_text) < 8:
            self.password_error.setText("✖  Password must be at least 8 characters long.")
            self.password_error.setVisible(True)
            self.set_password_style(self.new_password)
            has_error = True

        if has_error:
            return

        try:
            hashed_pw = bcrypt.hashpw(password_text.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE teachers 
                    SET password_hash = ?, is_synced = 0 
                    WHERE email = ?
                """, (hashed_pw, email_text))
                
                cursor.execute("""
                    INSERT INTO sync_queue (table_name, record_id, action)
                    SELECT 'teachers', teacher_id, 'UPDATE' FROM teachers WHERE email = ?
                """, (email_text,))
                
                conn.commit()

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Success")
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText("Your password has been successfully reset! You can now log in.")
            msg_box.setStyleSheet(f"""
                QMessageBox {{ 
                    background-color: {LIGHT}; 
                    font-family: {BODY_FONT}; 
                    font-size: 16px; 
                }}
                QMessageBox QLabel {{ 
                    color: {CHOCO_BROWN}; 
                }}
                QPushButton {{ 
                    background-color: {CORAL_RED}; 
                    color: {LIGHT}; 
                    font-weight: 700; 
                    padding: 6px 16px; 
                    border-radius: 4px; 
                }}
            """)
            msg_box.exec()

            self.router.navigate("login")

        except Exception as e:
            print(f"--> Database password reset error: {e}")
            self.email_error.setText("✖  An error occurred while resetting password.")
            self.email_error.setVisible(True)