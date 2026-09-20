import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import * 
from themes.fonts import BODY_FONT
from components.choices_button import ChoicesButton


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "salita")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")



class Salita10Game(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        #top layout| back buttonnnn
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(60, 50, 0, 20)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter  )

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("salita"))

        pagsasanay = QLabel("Pagsasanay 10: Pangungusap")
        pagsasanay.setStyleSheet(f"""
            font-size: 30px;
            font-family: {BODY_FONT};
            font-weight: 600;
            color: {CHOCO_BROWN};               
        """)

        top_layout.addWidget(back_btn)
        top_layout.addWidget(pagsasanay)
        top_layout.setSpacing(30)
        main_layout.addLayout(top_layout)

        title = QLabel("Si ______ ay nagluluto ng masarap na ulam.")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 32px; font-weight: 700; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)
        
        #image and choices
        choices = QHBoxLayout()
        main_layout.addLayout(choices)
        choices.setContentsMargins(0, 50, 0, 0)
        choices.addSpacing(50)

        # Illustration
        image = QLabel()
        image.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "nagluluto.png")).scaled(
                350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        image.setAlignment(Qt.AlignCenter)
        choices.addWidget(image)


        # Choices Layout
        quest_row = QVBoxLayout()
        quest_row.setSpacing(30)
        quest_row.setAlignment(Qt.AlignCenter)

        self.opt_1 = ChoicesButton("kuya", color=CORNFLOWER_BLUE)  # Correct
        self.opt_2 = ChoicesButton("nanay", color=MEDIUM_PURPLE)     # Wrong
        self.opt_3 = ChoicesButton("bunso", color=HONEY_YELLOW)     # Correct

        self.opt_1.clicked.connect(lambda: self.handle_choice(True, self.opt_1, "matamis"))
        self.opt_2.clicked.connect(lambda: self.handle_choice(False, self.opt_2, "maalat"))
        self.opt_3.clicked.connect(lambda: self.handle_choice(True, self.opt_3, "malamig"))

        quest_row.addWidget(self.opt_1)
        quest_row.addWidget(self.opt_2)
        quest_row.addWidget(self.opt_3)
        choices.addLayout(quest_row)


        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(200)
        lower_layout.setContentsMargins(70, 20, 70, 30)
        main_layout.addLayout(lower_layout)

        self.next_btn = QPushButton("Sunod")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
            background-color: {BRIGHT_YELLOW};
            color: {CHOCO_BROWN};
            font-size: 22px;
            font-weight: 700;
            border-radius: 6px;
            font-family: {BODY_FONT};
        """)
        self.next_btn.setFixedSize(180, 50)
        lower_layout.addWidget(self.next_btn, alignment = Qt.AlignmentFlag.AlignRight)
        self.next_btn.clicked.connect(lambda: self.router.navigate("salitaq9"))


