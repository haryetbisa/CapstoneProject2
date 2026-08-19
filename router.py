from PySide6.QtWidgets import QStackedWidget, QWidget


class Router:
    """Handles switching between screens by name."""

    def __init__(self, stacked_widget: QStackedWidget):
        self.stack = stacked_widget
        self.routes: dict[str, QWidget] = {}

    def register(self, name: str, widget: QWidget):
        """Add a screen and give it a name."""
        self.routes[name] = widget
        self.stack.addWidget(widget)

    def navigate(self, name: str):
        """Show the screen with this name safely."""
        if name in self.routes:
            self.stack.setCurrentWidget(self.routes[name])
        else:
            print(f"[Router Error] Screen route '{name}' does not exist!")