import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # this IS assets/ now
IMAGE_DIR = os.path.join(BASE_DIR, "image")

def icon_label(filename, size=48, align=None):
    icon = QLabel()
    icon.setPixmap(
        QPixmap(os.path.join(IMAGE_DIR, filename)).scaled(
            size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
    )
    if align:
        icon.setAlignment(align)
    return icon