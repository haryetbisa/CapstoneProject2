from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPushButton, QLineEdit
from PySide6.QtGui import QPixmap, QColor, QPalette
from PySide6.QtCore import QRect


from components.cardsbutton import CardsButton
from themes.colors import *
from assets.icon import icon_label
from themes.fonts import  HEADING_FONT, BODY_FONT
from assets.icon import icon_label

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "assets", "image")
ICONS_DIR = os.path.join(BASE_DIR, "..", "assets", "icons")


class AccountInfo(QWidget):
    def __init__(self,router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(QPixmap(QPixmap(os.path.join(IMAGE_DIR, "logo.png")).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        main_layout.addWidget(logo)


        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.setSpacing(10)
        main_layout.addLayout(input_layout)

        create = QLabel("Create an account")
        create.setAlignment(Qt.AlignmentFlag.AlignLeft)
        create.setStyleSheet(f"font-family: {BODY_FONT}; color: {CHOCO_BROWN}; font-weight: 600; font-size: 18px;")
        input_layout.addWidget(create)

        email_label = QLabel("Email")
        email_label.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;")
        email_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_layout.addWidget(email_label)
        
        email = QLineEdit()
        email.setFixedSize(888, 64)
        email.setPlaceholderText("name@gmail.com")
        email.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        palette = email.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        email.setPalette(palette)
        

        email.setStyleSheet(f"""
            QLineEdit{{
            font-family: {BODY_FONT};
            font-size: 18px;
            color: {CHOCO_BROWN};
            border: 2px solid {CORAL_RED};        
            border-radius: 4px;
            background-color: {LIGHT}; 
            padding: 12px 16px;        
         }} """)
        input_layout.addWidget(email)

        pass_label = QLabel("Password")
        pass_label.setStyleSheet(f"font-family: {BODY_FONT}; font-size: 16px; color: {CORAL_RED}; font-weight: 500;")
        pass_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_layout.addWidget(pass_label)


        password = QLineEdit()
        password.setFixedSize(888, 64)
        password.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        password.setPlaceholderText("********")
        password.setEchoMode(QLineEdit.Password)

        palette = password.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(CHOCO_BROWN))
        password.setPalette(palette)

        password.setStyleSheet(f"""
            QLineEdit{{
            font-family: {BODY_FONT};
            font-size: 18px;
            color: {CHOCO_BROWN};
            border: 2px solid {CORAL_RED};        
            border-radius: 6px;
            background-color: {LIGHT}; 
            padding: 12px 16px;              
         }} """)
        input_layout.addWidget(password)


        create_btn = QPushButton("Create account")
        create_btn.setFixedSize(340,60)
        create_btn.setStyleSheet(
            f"""QPushButton{{
                background-color: {CORAL_RED};
                color: {LIGHT};
                font-family: {BODY_FONT};
                font-size: 24px;
                font-weight: 900px;
                padding: 2px 6px;
                border-radius: 6px;
        }}""")
        create_btn.clicked.connect(lambda: self.router.navigate("home"))
        main_layout.addWidget(create_btn, alignment = Qt.AlignmentFlag.AlignCenter)


        original = QPixmap("assets/images/together_kids.png")
                # copy(x, y, width, height) — crop starting at (x, y), taking that much width/height
        cropped = original.copy(0, 0, 300, 200)


        image_bottom = QHBoxLayout()
        image_bottom.setSpacing(10)
        image_bottom.setContentsMargins(0, 5, 0, 0)
  
        kids1 = QLabel()
        kids1.setPixmap(QPixmap(QPixmap(os.path.join(IMAGE_DIR, "kids2.png")).scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        kids1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        image_bottom.addWidget(kids1)


        kids2 = QLabel()
        kids2.setPixmap(QPixmap(QPixmap(os.path.join(IMAGE_DIR, "kids1.png")).scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        kids2.setAlignment(Qt.AlignmentFlag.AlignRight)
        image_bottom.addWidget(kids2)

        
        kids1 = QLabel()
        kids1.setPixmap(QPixmap(QPixmap(os.path.join(IMAGE_DIR, "kids2.png")).scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        kids1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        image_bottom.addWidget(kids1)
        
        
        kids2 = QLabel()
        kids2.setPixmap(QPixmap(QPixmap(os.path.join(IMAGE_DIR, "kids1.png")).scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        kids2.setAlignment(Qt.AlignmentFlag.AlignRight)
        image_bottom.addWidget(kids2)

        main_layout.addLayout(image_bottom)




        

