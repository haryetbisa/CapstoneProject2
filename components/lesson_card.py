from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from themes.colors import *
from themes.fonts import BODY_FONT


class LessonCard(QWidget):
    def __init__(self, title: str, body_text: str):
        super().__init__()

        self.setFixedSize(486, 494)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Outer container — gives the whole card its border + overall rounding
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.setStyleSheet(f"""
            LessonCard {{
                background-color: {WHITE};
                border: 2px solid {BLACK};
                border-radius: 10px;
            }}
        """)

        # ---- Header 
        header = QLabel(title)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"""
            background-color: #FFD24C;
            color: {CHOCO_BROWN};
            font-family: {BODY_FONT};
            font-size: 24px;
            font-weight: 700;

            border-top: 2px solid #000000;
            border-left: 2px solid #000000;
            border-right: 2px solid #000000;
            border-bottom: 2px solid #000000;

            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            min-height: 80px;
            max-height: 80px;
        """)
        outer_layout.addWidget(header)

# ---- Body (scrollable) ----
        body = QLabel(body_text)
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignCenter)
        body.setStyleSheet(f"""
            background: transparent;
            color: {BLACK};
            font-family: {BODY_FONT};
            font-size: 22px;
            padding: 40px 40px;
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
        QScrollArea { background: transparent; border: none; }
        QScrollArea > QWidget > QWidget { background: transparent; }
    """)
        scroll.setWidget(body)
        outer_layout.addWidget(scroll)

