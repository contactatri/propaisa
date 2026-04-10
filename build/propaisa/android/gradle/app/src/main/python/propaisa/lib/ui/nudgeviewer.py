from functools import partial
from pathlib import Path
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from lib.ui.togahelper import TogaHelper
from lib.entity.expense import Expense, Nudge
from lib.entity.expense_manager import ExpenseManager

class NudgeViewer:
    def __init__(self, app, userid, script_dir, icons_dir):
        self.app = app
        self.userid = userid
        self.script_dir = script_dir
        self.icons_dir = icons_dir
    def get_nudge_box (self, expense_id:int=0):
        nudge_box=toga.Box(style=Pack(direction=COLUMN,flex=1, background_color="#fff"))
        expense_manager = ExpenseManager(f"{self.script_dir}/propaisa.db",self.userid)
        #expenses = expense_manager.view_expenses()
        print(f"Loaded {len(expense_manager.expenses)} expenses for user ID {self.userid} ")
        for expense in expense_manager.expenses:
            if(expense_id!=0 and expense.id!=expense_id):
                continue
            for nudge in expense.nudges:
                label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
                if(nudge.sentiment==-1):
                    red_bulb_icon_path = f"{self.icons_dir}/red_bulb.png" 
                    #red_bulb_icon_path = "C:/dev/py/beeware/propaisa/src/propaisa/icons/red_bulb.png"
                    red_bulb_icon_image = toga.Image(red_bulb_icon_path)
                    red_bulb_icon_widget = toga.ImageView(image=red_bulb_icon_image, style=Pack(width=32, height=32, padding_right=5))
                    expense_label = toga.Label(
                        f"{nudge.message}",
                        margin=(0, 5),
                        style=Pack(color="red")
                    )
                    label_with_icon_box.add(red_bulb_icon_widget)
                    label_with_icon_box.add(expense_label)
                elif(nudge.sentiment==1):
                    green_bulb_icon_path = f"{self.icons_dir}/green_bulb.png" 
                    #green_bulb_icon_path = "C:/dev/py/beeware/propaisa/src/propaisa/icons/green_bulb.png"
                    print(f"Green bulb icon path: {green_bulb_icon_path}")
                    green_bulb_icon_image = toga.Image(green_bulb_icon_path)
                    green_bulb_icon_widget = toga.ImageView(image=green_bulb_icon_image, style=Pack(width=32, height=32, padding_right=5))
                    expense_label = toga.Label(
                        f"{nudge.message}",
                        margin=(0, 5),
                        style=Pack(color="green")
                    )
                    label_with_icon_box.add(green_bulb_icon_widget)
                    label_with_icon_box.add(expense_label)
                else:
                    orange_bulb_icon_path = f"{self.icons_dir}/yellow_bulb.png" 
                    #orange_bulb_icon_path = "C:/dev/py/beeware/propaisa/src/propaisa/icons/yellow_bulb.png"
                    orange_bulb_icon_image = toga.Image(orange_bulb_icon_path)
                    orange_bulb_icon_widget = toga.ImageView(image=orange_bulb_icon_image, style=Pack(width=32, height=32, padding_right=5))
                    expense_label = toga.Label(
                        f"{nudge.message}",
                        margin=(0, 5),
                        style=Pack(color="orange")
                    )
                    label_with_icon_box.add(orange_bulb_icon_widget)
                    label_with_icon_box.add(expense_label)
                nudge_box.add(label_with_icon_box)
        return nudge_box