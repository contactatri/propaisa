from functools import partial
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from lib.ui.togahelper import TogaHelper
from lib.ui.bodyhelper import BodyHelper
class HeaderHelper:
    def __init__(self, app):
        self.app = app
        #self.header_box = toga.Box(style=Pack(height=50, background_color="#ddd"))
    
    
    # Helper method accepting the widget AND a string
    