import os
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from themes.colors import * 
from themes.fonts import BODY_FONT
from components.choices_button import ChoicesButton


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "image_content", "bilang_g1")
ICONS_DIR = os.path.join(BASE_DIR, "..", "..", "..", "assets", "icons")


class LessonMath5(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 30, 40, 30)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)

        # Top layout | back button
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(60, 50, 0, 20)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "back_arrow.png")))
        back_btn.setFlat(True)
        back_btn.setIconSize(QSize(40, 40))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"border: none; background-color: none; border-radius: 6px")
        back_btn.clicked.connect(lambda: self.router.navigate("bilang_g1"))

        pagsasanay = QLabel("Aralin: Laktaw na Pagbilang (Skip Counting)")
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

        # Title
        title = QLabel("Pagbilang ng Dalawahan")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 30px; font-weight: 600; font-family: {BODY_FONT}; color: {CHOCO_BROWN};")
        main_layout.addWidget(title)

        # Text row
        text_row = QHBoxLayout()
        text_row.setSpacing(5)

        lesson_text = QLabel(
            "Sa Pagbilang ng Dalawahan, magdadagdag tayo ng dalawang bilang upang "
            "makuha ang kasunod na bilang."
        )
        lesson_text.setAlignment(Qt.AlignCenter)
        lesson_text.setWordWrap(True)   
        lesson_text.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 400;
            font-family: {BODY_FONT};
            color: {CHOCO_BROWN};
        """)
        text_row.addWidget(lesson_text)

        main_layout.addLayout(text_row)

        # Illustration
        example_image = QHBoxLayout()
        example_image.setSpacing(1)
        main_layout.addLayout(example_image)

        pic1 = QLabel()
        pic1.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "dalawahan_2.png")).scaled(
                280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        pic1.setAlignment(Qt.AlignCenter)
        example_image.addWidget(pic1)

        pic2 = QLabel()
        pic2.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "dalawahan_4.png")).scaled(
                280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        pic2.setAlignment(Qt.AlignCenter)
        example_image.addWidget(pic2)

        pic3 = QLabel()
        pic3.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "dalawahan_6.png")).scaled(
                280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        pic3.setAlignment(Qt.AlignCenter)
        example_image.addWidget(pic3)

        pic4 = QLabel()
        pic4.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "dalawahan_8.png")).scaled(
                280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        pic4.setAlignment(Qt.AlignCenter)
        example_image.addWidget(pic4)

        pic5 = QLabel()
        pic5.setPixmap(
            QPixmap(os.path.join(IMAGE_DIR, "dalawahan_10.png")).scaled(
                280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        pic5.setAlignment(Qt.AlignCenter)
        example_image.addWidget(pic5)

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
        lower_layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignRight)
        self.next_btn.clicked.connect(lambda: self.router.navigate("dalawahan_quest1"))

        main_layout.addStretch()