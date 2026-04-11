from functools import partial
import traceback
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from lib.ui.togahelper import TogaHelper
from pathlib import Path
from lib.ui.nudgeviewer import NudgeViewer
from lib.ui.expensecontroller import ExpenseController
from lib.entity.visualization_manager import VisualizationManager
from lib.entity.expense import Expense, Nudge
class LoginController:
    def __init__(self, app):
        self.app = app
        self.toga_helper = TogaHelper(app)
    
    def pre_login_screen(self):
        return_box=toga.Box(direction=COLUMN)
        self.webview = toga.WebView(style=Pack(flex=1))
        html_path = f"{self.app.script_dir}\T&C.html"
        print(f"Loading HTML content from: {html_path}")
        #self.webview.url = f"file://{html_path}"
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            # Load the content into the WebView
            self.webview.set_content("http://localhost", html_content)
        except Exception as e:
            self.webview.set_content("http://localhost", f"<html><body>Error loading file: {e}</body></html>")
        '''
        name_label = toga.Label(
            "Your name: ",
            margin=(0, 5),
        )
        password_label = toga.Label(
            "Your Password: ",
            margin=(0, 5),
        )
        '''
        #self.name_input = toga.TextInput(style=Pack(padding_top=1))
        #self.password_inp = toga.PasswordInput(style=Pack(padding_top=1)) # Use toga.PasswordInput
        #login_box = toga.Box(direction=ROW, margin=5)
        #login_box.add(self.webview)
        #login_box.add(name_label)
        #login_box.add(self.name_input)
        #login_box.add(password_label)
        #login_box.add(self.password_inp)

        button = toga.Button(
            "I Agree",
            #on_press=partial(self.toga_helper.show_alert, message_str="Hello from helper"),
            on_press=partial(self.login_action),
            margin=5,
        )
        return_box.add(self.webview)
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
        command_expense_visualization = toga.Command(
            self.menu_expense_visualization_handler,
            text='Expense Visualizations',
            tooltip='View expense visualizations',
            shortcut=toga.Key.MOD_1 + 'v',
            group=visualization_group,
            section=10
        )
        self.app.commands.add(command_expense_visualization) # Add the command to the application
        command_interest_visualization = toga.Command(
            self.menu_interest_visualization_handler,
            text='Interest Visualizations',
            tooltip='View interest visualizations',
            shortcut=toga.Key.MOD_1 + 'i',
            group=visualization_group,
            section=10
        )
        self.app.commands.add(command_interest_visualization) # Add the command to the application
        command_income_expense_visualization = toga.Command(
            self.menu_income_expense_visualization_handler,
            text='Income-Expense Visualizations',
            tooltip='View income and expense visualizations',
            shortcut=toga.Key.MOD_1 + 'e',
            group=visualization_group,
            section=10
        )
        self.app.commands.add(command_income_expense_visualization) # Add the command to the application

        ########################################
        expense_controller = ExpenseController(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
        self.app.main_box.add(expense_controller.expense_dashboard_screen())
        self.app.main_window.content = self.app.main_box
        self.app.main_window.show()
    def menu_clear_expenses_handler(self, sender, **kwargs):
        try:
            expense_controller = ExpenseController(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
            expense_controller.clear_table("user_expense")
            self.app.main_window.info_dialog("Action", "Clear Expenses executed suvccessfully!")
        except Exception as e:
            print("--- Full Traceback ---")
            traceback.print_exc() 
            print("----------------------")
            self.app.main_window.error_dialog("Error", f"An error occurred while clearing expenses: {e}")
    def menu_export_expenses_handler(self, sender, **kwargs):
        try:
            expense_controller = ExpenseController(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
            expense_controller.export_expense_list()
            self.app.main_window.info_dialog("Action", "Export Expenses successful!")
        except Exception as e:
            print("--- Full Traceback ---")
            traceback.print_exc()
            print("----------------------")
            self.app.main_window.error_dialog("Error", f"An error occurred while exporting expenses: {e}")
    def menu_import_expenses_handler(self, sender, **kwargs):
        try:
            expense_controller = ExpenseController(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
            expense_controller.import_expense_list("expenses_import.xlsx")
            self.app.main_window.info_dialog("Action", "Import Expenses succesful!")
        except Exception as e:
            print("--- Full Traceback ---")
            traceback.print_exc()
            print("----------------------")
            self.app.main_window.error_dialog("Error", f"An error occurred while importing expenses: {e}")
    def menu_expense_visualization_handler(self, sender, **kwargs):
        #self.app.main_window.info_dialog("Action", "Visualization menu item was clicked!")
        visualization_manager = VisualizationManager(f"{self.app.script_dir}/propaisa.db")
        visualization_manager.plot_expense_trends()
    def menu_interest_visualization_handler(self, sender, **kwargs):
        #self.app.main_window.info_dialog("Action", "Visualization menu item was clicked!")
        visualization_manager = VisualizationManager(f"{self.app.script_dir}/propaisa.db")
        visualization_manager.plot_interest_trends()
    def menu_income_expense_visualization_handler(self, sender, **kwargs):
        #self.app.main_window.info_dialog("Action", "Visualization menu item was clicked!")
        visualization_manager = VisualizationManager(f"{self.app.script_dir}/propaisa.db")
        visualization_manager.plot_income_expense_trends()
