from datetime import datetime, date, time
from functools import partial
from pathlib import Path
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from lib.ui.togahelper import TogaHelper
from lib.entity.expense import Expense, Nudge
from lib.entity.expense_manager import ExpenseManager
from lib.ui.nudgeviewer import NudgeViewer
class ExpenseController:
    
    def __init__(self, app,userid, script_dir, icons_dir):
        self.app = app
        self.userid = userid
        self.script_dir = script_dir
        self.icons_dir = icons_dir
        self.label_Pack = Pack(color="black", font_size=12, font_weight="bold")
        self.input_Pack = Pack(color="black", font_size=12, font_weight="bold", flex=1)
        self.widget_Pack=Pack(width=20, height=20, padding_right=5)
    
    def on_select_handler(self, widget):
        selected_row = widget.selection
        if selected_row:
            print(f"Selected Item: {selected_row}")
            self.app.main_box.clear()
            self.app.main_box.add(self.app.get_header_box())
            expense_object=None
            if selected_row.id == -1:
                #Create New Expense Object
                expense_object = Expense()
                self.app.main_box.add(self.get_expense_box(expense_object))
            elif selected_row.id == -2:
                #Create New Income Object
                self.app.main_box.add(self.get_enter_income_box())
            else:
                expense_object = Expense(
                    id=selected_row.id, 
                    name=selected_row.name, 
                    amount=selected_row.amount, 
                    savedamount=selected_row.saved_amount,
                    settledamount=selected_row.settled_amount,
                    duedate=selected_row.due_date
                )
                nudge_viewer = NudgeViewer(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
                nudge_box = toga.Box(style=Pack(direction=COLUMN,flex=1, background_color="#fff"))
                nudge_box.add(self.get_expense_box(expense_object))
                nudge_box.add(nudge_viewer.get_nudge_box(expense_object.id))
                
                scroll_container = toga.ScrollContainer(
                    content=nudge_box
                    ,style=Pack(flex=1,direction=COLUMN)
                    ,horizontal=True
                    , vertical=True
                )
                self.app.main_box.add(scroll_container)

            self.app.main_window.content = self.app.main_box
            self.app.main_window.show()
    def get_enter_income_box (self):
        body_box=toga.Box(style=Pack(direction=COLUMN,flex=1, background_color="#fff"))
        #Field Amount#####################
        amount_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
        amount_input_icon_path = f"{self.icons_dir}/amount.png" 
        amount_input_icon_image = toga.Image(amount_input_icon_path)
        amount_input_icon_widget = toga.ImageView(image=amount_input_icon_image, style=self.widget_Pack)
        amount_input_label = toga.Label(
            f"Amount",
            margin=(0, 5),
            style=self.label_Pack
        )
        amount_input = toga.TextInput(value=0, style=self.input_Pack)
        amount_input_label_with_icon_box.add(amount_input_icon_widget)
        amount_input_label_with_icon_box.add(amount_input_label)
        amount_input_label_with_icon_box.add(amount_input)
        body_box.add(amount_input_label_with_icon_box)
        ##########################################
        #Field Due Date#####################
        due_date_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
        due_date_input_icon_path = f"{self.icons_dir}/duedate.png" 
        due_date_input_icon_image = toga.Image(due_date_input_icon_path)
        due_date_input_icon_widget = toga.ImageView(image=due_date_input_icon_image, style=self.widget_Pack)
        due_date_input_label = toga.Label(f"Income Date",margin=(0, 5), style=self.label_Pack)

        date_input = toga.DateInput(on_change=self.on_date_change,style=Pack(padding=10))
        due_date_input_label_with_icon_box.add(due_date_input_icon_widget)
        due_date_input_label_with_icon_box.add(due_date_input_label)
        due_date_input_label_with_icon_box.add(date_input)
        body_box.add(due_date_input_label_with_icon_box)
        ##########################################
        ##########################################
        button = toga.Button(
            "Enter Income",
            #on_press=partial(self.update_action,amount_input.value,saved_amount_input.value,settled_amount_input.value),
            on_press=lambda *args: self.income_action(amount_input.value, date_input.value),
            margin=5,
        )
        body_box.add(button)
        return body_box

    def get_expense_list_box (self):
        #expense_list_box=toga.Box(style=Pack(flex=1,direction=COLUMN))
        expense_manager = ExpenseManager(f"{self.script_dir}/propaisa.db",self.userid)
        #expenses = expense_manager.view_expenses()

        print(f"Loaded {len(expense_manager.expenses)} expenses for user ID {self.userid}")
        expense_data=[]
        for expense in expense_manager.expenses:
            expense_tuple=(expense.name, expense.amount, expense.savedamount, expense.settledamount, expense.gapamount, expense.daily_saving_amount, expense.projected_yearly_interest, expense.duedate, expense.id)
            expense_data.append(expense_tuple)
        expense_tuple=("Create New Expense", 0, 0, 0, 0, 0, 0, str(datetime.now()), -1)
        income_tuple=("Create New Income", 0, 0, 0, 0, 0, 0, str(datetime.now()), -2)
        expense_data.append(expense_tuple)
        expense_data.append(income_tuple)
        #content_box = toga.Box(style=Pack(direction=COLUMN))
        table = toga.Table(
            headings=['Name', 'Amount', 'Saved Amount', 'Settled Amount', 'Gap Amount', 'Daily Saving Amount', 'Projected Yearly Interest', 'Due Date', 'ID'],
            data=expense_data,
            on_select=self.on_select_handler, # Pass the handler function
            multiple_select=False, # Set to True for multiple selections
            style=Pack(flex=1,padding=5, background_color="#fff")
        )
        return table
    def expense_dashboard_screen (self):
        body_box=toga.Box(style=Pack(direction=COLUMN,flex=1, background_color="#fff"))
        #nudge_viewer = NudgeViewer(self.app, self.app.userid, self.app.script_dir, self.app.icons_dir)
        #nudge_box = nudge_viewer.get_nudge_box()
        #body_box.add(nudge_box)
        body_box.add(self.get_expense_list_box())
        empty_box = toga.Box(style=Pack(height=5))
        scroll_container = toga.ScrollContainer(
            content=empty_box
            ,style=Pack(flex=1,direction=COLUMN)
            ,horizontal=False
            , vertical=True
        )

        body_box.add(scroll_container)
        return body_box
    def get_expense_box(self, expense:Expense=None):
        expense_box=toga.Box(style=Pack(direction=COLUMN,flex=1, background_color="#fff"))
        try:
            #Field ID #####################
            
            
            id_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            id_icon_path = f"{self.icons_dir}/ID.png" 
            id_icon_image = toga.Image(id_icon_path)
            id_icon_widget = toga.ImageView(image=id_icon_image, style=self.widget_Pack)
            id_label = toga.Label(
                f"ID",
                margin=(0, 5),
                style=self.label_Pack
            )
            id_value_label = toga.Label(
                f"{expense.id}",
                margin=(0, 5),
                style=self.label_Pack
            )
            id_label_with_icon_box.add(id_icon_widget)
            id_label_with_icon_box.add(id_label)
            id_label_with_icon_box.add(id_value_label)
            expense_box.add(id_label_with_icon_box)
            ##########################################
            #Field Expense Name#####################
            expense_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            expense_icon_path = f"{self.icons_dir}/expense.png" 
            expense_icon_image = toga.Image(expense_icon_path)
            expense_icon_widget = toga.ImageView(image=expense_icon_image, style=self.widget_Pack)
            expense_label = toga.Label(
                f"Expense Name",
                margin=(0, 5),
                style=self.label_Pack
            )
            name_input = toga.TextInput(value=f"{expense.name}", style=self.input_Pack)
            expense_label_with_icon_box.add(expense_icon_widget)
            expense_label_with_icon_box.add(expense_label)
            expense_label_with_icon_box.add(name_input)
            expense_box.add(expense_label_with_icon_box)
            ##########################################
            #Field Amount#####################
            amount_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            amount_input_icon_path = f"{self.icons_dir}/amount.png" 
            amount_input_icon_image = toga.Image(amount_input_icon_path)
            amount_input_icon_widget = toga.ImageView(image=amount_input_icon_image, style=self.widget_Pack)
            amount_input_label = toga.Label(
                f"Amount",
                margin=(0, 5),
                style=self.label_Pack
            )
            amount_input = toga.TextInput(value=f"{expense.amount}", style=self.input_Pack)
            amount_input_label_with_icon_box.add(amount_input_icon_widget)
            amount_input_label_with_icon_box.add(amount_input_label)
            amount_input_label_with_icon_box.add(amount_input)
            expense_box.add(amount_input_label_with_icon_box)
            ##########################################
            #Field Saved Amount#####################
            saved_amount_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            saved_amount_input_icon_path = f"{self.icons_dir}/savedamount.png" 
            saved_amount_input_icon_image = toga.Image(saved_amount_input_icon_path)
            saved_amount_input_icon_widget = toga.ImageView(image=saved_amount_input_icon_image, style=self.widget_Pack)
            saved_amount_input_label = toga.Label(
                f"Saved Amount",
                margin=(0, 5),
                style=self.label_Pack
            )
            saved_amount_input = toga.TextInput(value=f"{expense.savedamount}", style=self.input_Pack)
            saved_amount_input_label_with_icon_box.add(saved_amount_input_icon_widget)
            saved_amount_input_label_with_icon_box.add(saved_amount_input_label)
            saved_amount_input_label_with_icon_box.add(saved_amount_input)
            expense_box.add(saved_amount_input_label_with_icon_box)
            ##########################################
            #Field Settled Amount#####################
            settled_amount_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            settled_amount_input_icon_path = f"{self.icons_dir}/savedamount.png" 
            settled_amount_input_icon_image = toga.Image(settled_amount_input_icon_path)
            settled_amount_input_icon_widget = toga.ImageView(image=settled_amount_input_icon_image, style=self.widget_Pack)
            settled_amount_input_label = toga.Label(
                f"Settled Amount",
                margin=(0, 5),
                style=self.label_Pack
            )
            settled_amount_input = toga.TextInput(value=f"{expense.settledamount}", style=self.input_Pack)
            settled_amount_input_label_with_icon_box.add(settled_amount_input_icon_widget)
            settled_amount_input_label_with_icon_box.add(settled_amount_input_label)
            settled_amount_input_label_with_icon_box.add(settled_amount_input)
            expense_box.add(settled_amount_input_label_with_icon_box)
            ##########################################
            #Field Gap Amount#####################
            gap_amount_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            gap_amount_input_icon_path = f"{self.icons_dir}/gapamount.png" 
            gap_amount_input_icon_image = toga.Image(gap_amount_input_icon_path)
            gap_amount_input_icon_widget = toga.ImageView(image=gap_amount_input_icon_image, style=self.widget_Pack)
            gap_amount_input_label = toga.Label(f"Gap Amount",margin=(0, 5),style=self.label_Pack)
            gap_amount_value_input_label = toga.Label(expense.gapamount,margin=(0, 5),style=self.label_Pack)
            gap_amount_input_label_with_icon_box.add(gap_amount_input_icon_widget)
            gap_amount_input_label_with_icon_box.add(gap_amount_input_label)
            gap_amount_input_label_with_icon_box.add(gap_amount_value_input_label)
            expense_box.add(gap_amount_input_label_with_icon_box)
            ##########################################
            #Field daily_saving_amount Amount#####################
            daily_saving_amount_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            daily_saving_amount_input_icon_path = f"{self.icons_dir}/savedamount.png" 
            daily_saving_amount_input_icon_image = toga.Image(daily_saving_amount_input_icon_path)
            daily_saving_amount_input_icon_widget = toga.ImageView(image=daily_saving_amount_input_icon_image, style=self.widget_Pack)
            daily_saving_amount_input_label = toga.Label(f"Daily Saving Amount",margin=(0, 5),style=self.label_Pack)
            daily_saving_amount_value_input_label = toga.Label(expense.daily_saving_amount,margin=(0, 5),style=self.label_Pack)
            daily_saving_amount_input_label_with_icon_box.add(daily_saving_amount_input_icon_widget)
            daily_saving_amount_input_label_with_icon_box.add(daily_saving_amount_input_label)
            daily_saving_amount_input_label_with_icon_box.add(daily_saving_amount_value_input_label)
            expense_box.add(daily_saving_amount_input_label_with_icon_box)
            ##########################################
            ##########################################
            #Field Interest Amount#####################
            interest_amount_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            interest_amount_input_icon_path = f"{self.icons_dir}/interest.png" 
            interest_amount_input_icon_image = toga.Image(interest_amount_input_icon_path)
            interest_amount_input_icon_widget = toga.ImageView(image=interest_amount_input_icon_image, style=self.widget_Pack)
            interest_amount_input_label = toga.Label(f"Interest Amount",margin=(0, 5), style=self.label_Pack)
            interest_value_amount_input_label = toga.Label(expense.projected_yearly_interest,margin=(0, 5), style=self.label_Pack)
            interest_amount_input_label_with_icon_box.add(interest_amount_input_icon_widget)
            interest_amount_input_label_with_icon_box.add(interest_amount_input_label)
            interest_amount_input_label_with_icon_box.add(interest_value_amount_input_label)
            expense_box.add(interest_amount_input_label_with_icon_box)
            ##########################################
            #Field Due Date#####################
            due_date_input_label_with_icon_box = toga.Box(style=Pack(direction=ROW, alignment="center"))
            due_date_input_icon_path = f"{self.icons_dir}/duedate.png" 
            due_date_input_icon_image = toga.Image(due_date_input_icon_path)
            due_date_input_icon_widget = toga.ImageView(image=due_date_input_icon_image, style=self.widget_Pack)
            due_date_input_label = toga.Label(f"Due Date",margin=(0, 5), style=self.label_Pack)
            due_date_amount_input = toga.TextInput(value=f"{expense.duedate}", style=self.input_Pack)
            due_date_value_input_label = toga.Label(expense.duedate,margin=(0, 5), style=self.label_Pack)
            date_input = toga.DateInput(on_change=self.on_date_change,style=Pack(padding=10))
            due_date_input_label_with_icon_box.add(due_date_input_icon_widget)
            due_date_input_label_with_icon_box.add(due_date_input_label)
            due_date_input_label_with_icon_box.add(due_date_value_input_label)
            due_date_input_label_with_icon_box.add(date_input)
            expense_box.add(due_date_input_label_with_icon_box)
            ##########################################
            button = toga.Button(
                "Update Expense",
                #on_press=partial(self.update_action,amount_input.value,saved_amount_input.value,settled_amount_input.value),
                on_press=lambda *args: self.update_action(expense.id, expense.name,amount_input.value,saved_amount_input.value,settled_amount_input.value, expense.duedate),
                margin=5,
            )
            expense_box.add(button)
            return expense_box
        except Exception as e:
            # This block catches all standard exceptions and stores the error in 'e'
            print(f"An exception of type {type(e).__name__} occurred: {e}")
    def on_date_change(self, widget):
        # This function is called when the date is changed
        print(f"Selected date: {widget.value}")
        selected_date = widget.value
        midnight_time = time.min # which is 00:00:00
        self.new_due_date=datetime.combine(selected_date, midnight_time)

    def update_action(self, expense_id, expense_name, amt, svd_amt,stld_amnt, duedate):
        try:
            expense_manager= ExpenseManager(f"{self.script_dir}/propaisa.db",self.userid)
            #Update expense object with new values from input fields
            print(f"Updating Expense ID: {expense_id} with Amount: {amt}, Saved Amount: {svd_amt}, Settled Amount: {stld_amnt}")
            if(self.new_due_date==None):
                self.new_due_date=duedate
            new_expense= Expense(
                id=expense_id,
                name=expense_name,
                amount=int(amt),
                savedamount=int(svd_amt),
                settledamount=int(stld_amnt),
                duedate=self.new_due_date
            )
            expense_manager.update_expense(new_expense)
            self.app.main_box.clear()
            self.app.main_box.add(self.app.get_header_box())    
            self.app.main_box.add(self.expense_dashboard_screen())
            self.app.main_window.content = self.app.main_box    
            self.app.main_window.show()
            
        except Exception as e:
            # This block catches all standard exceptions and stores the error in 'e'
            print(f"An exception of type {type(e).__name__} occurred: {e}")
    
    
    
