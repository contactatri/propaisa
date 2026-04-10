from functools import partial
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from lib.ui.togahelper import TogaHelper
class FooterHelper:
    def __init__(self, app, toga_helper: TogaHelper):
        self.app = app
        self.footer_box = toga.Box(style=Pack(height=50, background_color="#eee"))
        self.toga_helper = toga_helper
    # Helper method accepting the widget AND a string
    def get_footer_box (self):
        
        self.footer_label = toga.Label(
            "Holder for the footer content",
            margin=(0, 5),
        )
        self.footer_box.add(self.footer_label)
        return self.footer_box