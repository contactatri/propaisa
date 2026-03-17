import toga
from toga.style.pack import COLUMN, ROW
class TogaHelper:
    def __init__(self, app):
        self.app = app
    # Helper method accepting the widget AND a string
    def show_alert(self, widget, message_str):
        print(f"show_alert called with widget ID: {widget.id} and message: {message_str}")
        self.app.main_window.info_dialog(
            "Alert",
            f"Widget ID: {widget.id}\nMessage: {message_str}"
        )