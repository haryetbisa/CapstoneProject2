# screens/home_screen.py
import os

from assets.icon import icon_label
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QIcon
from themes.colors import *
from themes.fonts import HEADING_FONT, BODY_FONT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets", "image")

class HomeScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router


        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 0)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Home Screen"))
        layout.addLayout(main_layout)

        container = QWidget()
        container.setStyleSheet("""
            background-color: #FFD24C; 
            border-radius: 14px;       
        """)
        
        inner_layout = QHBoxLayout(container)
        inner_layout.setContentsMargins(20, 15, 20, 15)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)


        self.hello_text = QLabel("Hello, Teacher!")
        self.hello_text.setStyleSheet(f"""
            font-size: 26px;
            font-family: {BODY_FONT};
            font-weight: 800;
            color: #3A2E1F;
        """)

        self.welcome_text = QLabel("Welcome to BasaMatika")
        self.welcome_text.setStyleSheet(f"""
            font-size: 12px;
            font-family: {BODY_FONT};
            font-weight: 500;
            color: #6B5A3A;
        """)

        text_layout.addWidget(self.hello_text)
        text_layout.addWidget(self.welcome_text)
        inner_layout.addLayout(text_layout)
        inner_layout.addStretch()

        self.g_icon = QPushButton()
        audio_icon_path = os.path.join(ASSETS_DIR, "giraffe.png")
        if os.path.exists(audio_icon_path):
            self.g_icon.setIcon(QIcon(audio_icon_path))
        self.g_icon.setIconSize(QSize(40, 40))
        self.g_icon.setCursor(Qt.PointingHandCursor)
        self.g_icon.setStyleSheet(
                    "border: none; background-color: transparent;"
                )
        self.g_icon.clicked.connect(lambda: self.router.navigate("settings"))
        inner_layout.addWidget(self.g_icon)

        main_layout.addWidget(container)


        #2nd red container
        redcontainer = QWidget()
        redcontainer.setStyleSheet("""
            background-color: #F3554A;
            border-radius: 14px;       
        """)
        
        r_container = QVBoxLayout(redcontainer)
        r_container.setContentsMargins(20, 20, 20, 20)
        

        quote_text = QLabel("BAWAT BATA BUMABASA")
        quote_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_text.setStyleSheet(f"""
            font-size: 60px;
            font-family: {HEADING_FONT};                
            font-weight: 800;
            color: {WHITE};
        """)

        r_container.addWidget(quote_text)
        main_layout.addWidget(redcontainer)
        main_layout.addStretch()

        
        lower_part = QHBoxLayout()
        lower_part.setAlignment(Qt.AlignmentFlag.AlignBottom)

        pinkg = icon_label("pink_g.png", 340)
        pinkg.setContentsMargins(0, 20, 0, 0)
        pinkg.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBaseline)
        
        #buttons 
        button_group = QVBoxLayout()
        button_group.setContentsMargins(0, 0, 0, 60)
        button_group.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)

        #kinder button
        self.kinder = QPushButton("KINDERGARTEN")
        self.kinder.setCursor(Qt.PointingHandCursor)
        self.kinder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.kinder.setMinimumSize(492, 86)
        self.kinder.setStyleSheet(f"""
            background-color: {YELLOW};
            font-size: 46px;
            font-family: {HEADING_FONT};
            font-weight: 800;
            color: {CORAL_RED};
            padding: 10px 10px;     
        """)
        self.kinder.clicked.connect(lambda: self.router.navigate("kindergarten"))

        #grade1 button
        self.grade1 = QPushButton("GRADE 1")
        self.grade1.setCursor(Qt.PointingHandCursor)
        self.grade1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.grade1.setMinimumSize(492, 86)
        self.grade1.setStyleSheet(f"""
            background-color: {ROSE_PINK};
            font-size: 46px;
            font-weight: 800;
            font-family: {HEADING_FONT};
            color: {YELLOW};
            padding: 10px 10px;
    
        """)
        self.grade1.clicked.connect(lambda: self.router.navigate("grade1_dash"))


        redb = icon_label("red_b.png", 340)
        redb.setContentsMargins(0, 20, 0, 0)
        redb.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        lower_part.addWidget(pinkg) 
        button_group.addWidget(self.kinder)
        button_group.addWidget(self.grade1)
        lower_part.addLayout(button_group)
        lower_part.addWidget(redb)
        main_layout.addLayout(lower_part)
   

        

      


