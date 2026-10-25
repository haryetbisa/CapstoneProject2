# screens/create_account.py

import os
import threading
import http.server
import socketserver
import urllib.parse
import webbrowser
import requests
import uuid

from PySide6.QtCore import Qt, QSize, Signal, QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtGui import QPixmap, QTransform, QIcon
from themes.colors import *
from themes.fonts import BODY_FONT
from session import AppSession
from Database.connection import get_db_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


def make_icon(filename, size=24):
    icon_path = os.path.join(ICONS_DIR, filename)
    if os.path.exists(icon_path):
        pixmap = QPixmap(icon_path).scaled(
            size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        return QIcon(pixmap)
    return QIcon()


class GoogleSplashBridge(QObject):
    auth_received = Signal(str)


class CreateAccount(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.google_bridge = GoogleSplashBridge()
        self.google_bridge.auth_received.connect(self.process_google_login)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(300)
        main_layout.addLayout(top_layout)

        # LEFT TOP KID
        left_top = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "yellow_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        left_top.setPixmap(pixmap)
        left_top.move(-160, -20)   
        left_top.show()
        top_layout.addWidget(left_top)

        # Logo
        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "logoo.png")).scaled(
                350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(logo)

        # RIGHT TOP KID
        right_top = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "red_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        right_top.setPixmap(pixmap)
        right_top.move(200, -20)
        right_top.show()
        top_layout.addWidget(right_top)

        main_layout.addStretch()

        subtitle = QLabel("Teachers learning tools for students,\nfor practicing basic Filipino reading and basic Math.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {CHOCO_BROWN}; font-size: 20px; font-weight: 500; font-family: {BODY_FONT};")
        main_layout.addWidget(subtitle)

        main_layout.addStretch()

        # Create Account Button
        create_btn = QPushButton("Create account")
        create_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED}; 
                color: {LIGHT}; 
                font-size: 20px; 
                font-weight: 600; 
                font-family: {BODY_FONT}; 
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        create_btn.clicked.connect(lambda: self.router.navigate("credentials"))
        create_btn.setFixedSize(300, 50)
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        main_layout.addWidget(create_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Log-in Button
        login_btn = QPushButton("Log-in")
        login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CORAL_RED}; 
                color: {LIGHT}; 
                font-size: 20px; 
                font-weight: 600; 
                font-family: {BODY_FONT}; 
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #d94338;
            }}
        """)
        login_btn.setFixedSize(300, 50)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.clicked.connect(lambda: self.router.navigate("login"))
        main_layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- "OR" Divider Layout ---
        or_layout = QHBoxLayout()
        or_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        or_layout.setSpacing(15)

        line_left = QLabel()
        line_left.setFixedSize(120, 2)
        line_left.setStyleSheet("background-color: #E0E0E0;")

        or_text = QLabel("or")
        or_text.setStyleSheet(f"font-family: {BODY_FONT}; color: #888888; font-size: 15px; font-weight: 600;")

        line_right = QLabel()
        line_right.setFixedSize(120, 2)
        line_right.setStyleSheet("background-color: #E0E0E0;")

        or_layout.addWidget(line_left)
        or_layout.addWidget(or_text)
        or_layout.addWidget(line_right)
        main_layout.addLayout(or_layout)

        # --- Continue with Google Button ---
        google_btn = QPushButton("  Continue with Google")
        google_icon_path = os.path.join(ICONS_DIR, "google_icon.png")
        if os.path.exists(google_icon_path):
            google_btn.setIcon(QIcon(google_icon_path))
        google_btn.setIconSize(QSize(24, 24))
        google_btn.setFixedSize(300, 50)
        google_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        google_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: {CHOCO_BROWN};
                font-family: {BODY_FONT};
                font-size: 18px;
                font-weight: 700;
                border: 2px solid #DDDDDD;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #F5F5F5;
            }}
        """)
        google_btn.clicked.connect(self.start_google_oauth)
        main_layout.addWidget(google_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.setSpacing(1000)
        bottom_layout.setContentsMargins(0, 10, 0, 0)

        # LEFT BOTTOM KID
        left_bottom = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "blue_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        left_bottom.setPixmap(pixmap)
        left_bottom.move(-100, -60)
        left_bottom.show()
        bottom_layout.addWidget(left_bottom)

        # RIGHT BOTTOM KID
        right_bottom = QLabel(self)
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "pink_kid.png")).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        right_bottom.setPixmap(pixmap)
        right_bottom.move(200, -60)
        right_bottom.show()
        bottom_layout.addWidget(right_bottom)

        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()

    def start_google_oauth(self):
        """Spins up a local callback server, opens the browser, and handles Google token exchange[cite: 10]."""
        bridge = self.google_bridge
        client_id = "949510230347-lej92b7akjbq7cohurgfmqn7bfs58smd.apps.googleusercontent.com"  
        client_secret = "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" 

        class OAuthHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                code = query_components.get("code", [None])[0]
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                if code:
                    self.wfile.write(b"<h3>Authentication successful! You can close this window.</h3>")
                    try:
                        token_url = "https://oauth2.googleapis.com/token"
                        payload = {
                            "code": code,
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "redirect_uri": "http://localhost:8080",
                            "grant_type": "authorization_code",
                        }
                        token_response = requests.post(token_url, data=payload)
                        token_data = token_response.json()
                        print(f"--> Token Response from Google: {token_data}")
                        
                        access_token = token_data.get("access_token")

                        if access_token:
                            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
                            headers = {"Authorization": f"Bearer {access_token}"}
                            user_info_response = requests.get(userinfo_url, headers=headers)
                            user_info = user_info_response.json()
                            print(f"--> User Info from Google: {user_info}")
                            
                            email = user_info.get("email")
                            if email:
                                bridge.auth_received.emit(email)
                        else:
                            print("--> Failed to get access_token from Google response.")
                    except Exception as ex:
                        print(f"--> Error exchanging token with Google: {ex}")
                else:
                    self.wfile.write(b"<h3>Authentication failed. No code received.</h3>")
                    print("--> No authorization code found in redirect URL.")

            def log_message(self, format, *args):
                pass

        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True

        def run_server():
            with ReusableTCPServer(("localhost", 8080), OAuthHandler) as httpd:
                httpd.handle_request()

        threading.Thread(target=run_server, daemon=True).start()
        
        params = {
            "client_id": client_id,
            "redirect_uri": "http://localhost:8080",
            "response_type": "code",
            "scope": "email profile"
        }
        oauth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        webbrowser.open(oauth_url)

    def process_google_login(self, email):
        """Verifies or auto-registers the Google email in the database and logs in."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT teacher_id, full_name, email FROM teachers WHERE email = ?",
                    (email,)
                )
                teacher = cursor.fetchone()

                if teacher:
                    AppSession.set_teacher(teacher_id=teacher["teacher_id"], full_name=teacher["full_name"], remember=True)
                    self.router.navigate("home")
                else:
                    # Register new teacher from Google OAuth
                    new_teacher_id = str(uuid.uuid4())
                    
                    # 1. Insert into local teachers table
                    cursor.execute(
                        "INSERT INTO teachers (teacher_id, full_name, email, password_hash, section_name, is_synced) VALUES (?, ?, ?, ?, ?, 0)",
                        (new_teacher_id, "Guro", email, "oauth_google_secured", "Kindergarten - Paharang")
                    )
                    
                    
                    cursor.execute(
                        "INSERT INTO sync_queue (table_name, record_id, action) VALUES ('teachers', ?, 'INSERT')",
                        (new_teacher_id,)
                    )
                    
                    conn.commit()
                    AppSession.set_teacher(teacher_id=new_teacher_id, full_name="Guro", remember=True)
                    self.router.navigate("home")
        except Exception as e:
            print(f"--> Google login database error: {e}")