from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

def add_drop_shadow(widget, blur=20, x_offset=0, y_offset=4, color=(0, 0, 0, 80)):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(*color))
    widget.setGraphicsEffect(shadow)