"""
This app helps daily wage workers manage their income and expenditure, guiding them towards financial independence.
"""
from functools import partial
import sys
import subprocess
from pathlib import Path
import threading
sys.path.insert(0, str(Path(__file__).parent))
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from lib.ui.togahelper import TogaHelper
from lib.ui.logincontroller import LoginController
  

class propaisa(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        #main_box = toga.Box(style=Pack(direction=COLUMN))
        # Add header box from HeaderHelper
        #header_helper = HeaderHelper(self)
        # Initialize helper and pass 'self' (the app)

        self.userid=-1
        self.script_dir = Path(__file__).parent.absolute()
        self.icons_dir = f"{str(self.script_dir).replace('\\', '/')}/icons"
        print(f"Script directory: {self.script_dir}")
        self.header_box = toga.Box(style=Pack(height=50, background_color="#ddd"))
        self.body_box = toga.Box(style=Pack(direction=COLUMN,flex=1, background_color="#fff"))
        self.toga_helper = TogaHelper(self)
        self.login_controller = LoginController(self)
        
        '''
        header_helper = HeaderHelper(self)
        #main_box.add(header_helper.get_header_box())
        #header=header_helper.get_header_box()
        self.header_box.add(header_helper.get_login_box())
        body_helper = BodyHelper(self)
        self.body_box.add(body_helper.on_login_screen())
        self.main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.main_box.add(self.header_box)
        
        '''
        
        
        self.main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.main_box.add(self.login_controller.pre_login_screen())
        self.main_window = toga.MainWindow(title=self.formal_name)

        self.main_window.content = self.main_box
        #self.main_window.on_close = self.on_close_app
        self.main_window.show()
        
    def get_header_box(self):
        header_box=toga.Box(style=Pack(height=50, background_color="#ddd"))
        logedin_user_label = toga.Label(
            f"Welcome, {self.app.user_name} to ProPaisa!",
            margin=(0, 5),
        )
        #self.header_box.clear()
        header_box.add(logedin_user_label)
        return header_box
    def say_hello(self, widget):
        print(f"Hello, {self.name_input.value}")
    def on_close_app(self, window):
        # Signal threads to stop
        self.stop_event.clear()
        # Optionally wait for thread to finish
        # self.my_thread.join()
        return True # Allow app to close
    
def main():
    return propaisa()
