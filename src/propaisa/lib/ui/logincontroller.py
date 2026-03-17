from functools import partial
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from lib.ui.togahelper import TogaHelper
from pathlib import Path
from lib.ui.nudgeviewer import NudgeViewer
from lib.ui.expensecontroller import ExpenseController
from lib.entity.expense import Expense, Nudge
class LoginController:
    def __init__(self, app):
        self.app = app
        self.toga_helper = TogaHelper(app)
    
    def pre_login_screen(self):
        return_box=toga.Box(direction=ROW, margin=5)
        name_label = toga.Label(
            "Your name: ",
            margin=(0, 5),
        )
        password_label = toga.Label(
            "Your Password: ",
            margin=(0, 5),
        )
        self.name_input = toga.TextInput(style=Pack(padding_top=1))
        self.password_inp = toga.PasswordInput(style=Pack(padding_top=1)) # Use toga.PasswordInput
        login_box = toga.Box(direction=ROW, margin=5)
        login_box.add(name_label)
        login_box.add(self.name_input)
        login_box.add(password_label)
        login_box.add(self.password_inp)

        button = toga.Button(
            "Login",
            #on_press=partial(self.toga_helper.show_alert, message_str="Hello from helper"),
            on_press=partial(self.login_action),
            margin=5,
        )
        return_box.add(login_box)
        return_box.add(button)
        return return_box
    
    def login_action(self, widget):
        self.app.userid = 1  # Simulate setting a user ID after login
        self.app.user_name = self.name_input.value
        self.app.main_box.clear()
        self.app.main_box.add(self.app.get_header_box())
        expense_controller = ExpenseController(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
        self.app.main_box.add(expense_controller.expense_dashboard_screen())
        self.app.main_window.content = self.app.main_box
        self.app.main_window.show()

        