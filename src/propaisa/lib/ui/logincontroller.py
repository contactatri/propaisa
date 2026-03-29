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
        ###########Add Menu Commands
        # Define the command and add it to the app commands
        maintanence_group = toga.Group('Maintanence', order=40)
        visualization_group = toga.Group('Visualization', order=41)
        command_clear_expenses = toga.Command(
            self.menu_clear_expenses_handler,
            text='Clear Expenses',
            tooltip='Clear all expense entries',
            shortcut=toga.Key.MOD_1 + 'c',
            #group=toga.Group.FILE,
            group=maintanence_group,
            section=10
        )
        self.app.commands.add(command_clear_expenses) # Add the command to the application
        command_export_expenses = toga.Command(
            self.menu_export_expenses_handler,
            text='Export Expenses',
            tooltip='Export expense entries',
            shortcut=toga.Key.MOD_1 + 'e',
            group=maintanence_group,
            section=10
        )
        self.app.commands.add(command_export_expenses) # Add the command to the application
        command_visualization = toga.Command(
            self.menu_visualization_handler,
            text='Visualization',
            tooltip='View expense visualizations',
            shortcut=toga.Key.MOD_1 + 'v',
            group=visualization_group,
            section=10
        )
        self.app.commands.add(command_visualization) # Add the command to the application

        ########################################
        expense_controller = ExpenseController(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
        self.app.main_box.add(expense_controller.expense_dashboard_screen())
        self.app.main_window.content = self.app.main_box
        self.app.main_window.show()
    def menu_clear_expenses_handler(self, sender, **kwargs):
        self.main_window.info_dialog("Action", "Clear Expenses menu item was clicked!")
    def menu_export_expenses_handler(self, sender, **kwargs):
        self.app.main_window.info_dialog("Action", "Export Expenses menu item was clicked!")
        expense_controller = ExpenseController(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
        expense_controller.export_expense_list()
    def menu_visualization_handler(self, sender, **kwargs):
        self.main_window.info_dialog("Action", "Visualization menu item was clicked!")
