import sqlite3
from datetime import datetime
import traceback
import pandas as pd
from typing import Dict, Any, ClassVar
from typing import List, Optional
from lib.entity.sqlitemanager import SQLiteManager 
from lib.entity.expense import Expense, Interest

# Define color codes as constants
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m' # Reset color

class ExpenseManager:
    """
    A class to set up the SQLite database with required tables for expense  management.
    """
    def __init__(self, db_file,userid=1):
        self.db_file = db_file
        self.userid = userid  # For demo purpose, assuming single user with userid = 1
        self.expenses = []
        self.get_expenses()
        #self.create_expense_category("Fashion", "Clothing, accessories, and related items")
        #self.get_interest_trends()
    def get_expenses_as_dataframe(self) -> pd.DataFrame:
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = "SELECT id,name,amount,savedamount,settledamount,duedate,userid,categoryid,frequencyid,status FROM user_expense WHERE userid = ?"
                rows = db.fetch_all(query, (self.userid,))
                # Define the format string matching the SQLite string format
                format_string = '%Y-%m-%d %H:%M:%S'
                if rows:                
                    for row in rows:
                        expense = Expense(row[0], row[1], row[2], row[3], row[4], datetime.strptime(row[5], format_string), row[6], row[7], row[8], row[9])
                        self.expenses.append(expense)
                    # Using map() with a lambda function
                    expense_list_map = list(map(lambda expense_obj: f"{expense_obj.id} |{expense_obj.name} | {str(expense_obj.amount)} | {str(expense_obj.savedamount)} | {str(expense_obj.settledamount)} | {str(expense_obj.status)} | {str(expense_obj.duedate)}", self.expenses))
                    #print(f"User_Expenses: {expense_list_map}")
                else:
                    print(f"No records found.")
            # Convert list of Expense objects to a DataFrame
            df = pd.DataFrame([vars(expense) for expense in self.expenses])
            return df
        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error
    def get_interest_trends(self) -> List[Interest]:
        list_interest=[]
        try:
            with SQLiteManager(self.db_file) as db:
                query = "SELECT strftime('%Y-%m', duedate) AS year_month,  SUM(amount) AS total FROM user_expense WHERE userid = ? and categoryid = ? GROUP BY year_month ORDER BY year_month "
                rows = db.fetch_all(query, (self.userid, 9))  # Assuming categoryid = 9 for interest
                # Define the format string matching the SQLite string format
                format_string = '%Y-%m-%d %H:%M:%S'
                if rows:                
                    for row in rows:
                        new_interest = Interest(row[0], row[1])
                        list_interest.append(new_interest)
                    # Using map() with a lambda function
                    interest_list_map = list(map(lambda interest_obj: f"{interest_obj.period} | {str(interest_obj.rate)}", list_interest))
                    print(f"User_Interests: {interest_list_map}")
                else:
                    print(f"No records found.")
            #print(f"Loaded {len(self.expenses)} expenses for user ID {self.userid}")
            return list_interest
        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
            return []
    def get_expenses(self) -> List[Expense]:
        try:
            self.expenses.clear()  # Clear existing expenses before loading new ones
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = "SELECT id,name,amount,savedamount,settledamount,duedate,userid,categoryid,frequencyid,status FROM user_expense WHERE userid = ? "
                rows = db.fetch_all(query, (self.userid,))
                # Define the format string matching the SQLite string format
                format_string = '%Y-%m-%d %H:%M:%S'
                if rows:                
                    for row in rows:
                        expense = Expense(row[0], row[1], row[2], row[3], row[4], datetime.strptime(row[5], format_string), row[6], row[7], row[8], row[9])
                        self.expenses.append(expense)
                    # Using map() with a lambda function
                    expense_list_map = list(map(lambda expense_obj: f"{expense_obj.id} |{expense_obj.name} | {str(expense_obj.amount)} | {str(expense_obj.savedamount)} | {str(expense_obj.settledamount)} | {str(expense_obj.status)} | {str(expense_obj.duedate)}", self.expenses))
                    #print(f"User_Expenses: {expense_list_map}")
                else:
                    print(f"No records found.")
            #print(f"Loaded {len(self.expenses)} expenses for user ID {self.userid}")
            return self.expenses
        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
            return []
    
    def view_expenses(self) :
        for expense in self.expenses:
            print("**********************************************************")
            print(f"Expense Id: {expense.id}, Name: {expense.name}, Due Date: {expense.duedate}")
            print(f"  Amount: {expense.amount}, Saved Amount: {expense.savedamount}, Settled Amount: {expense.settledamount}")
            print(f"  Gap Amount: {expense.gapamount}, Daily Saving Amount: {expense.daily_saving_amount}, Projected Yearly Interest: {expense.projected_yearly_interest}")
            print("  Nudges:")
            for nudge in expense.nudges:
                if nudge.sentiment == -1:
                    print(f"{Colors.RED}Nudge Id: {nudge.id}, Name: {nudge.name}, Nudge Date: {nudge.nudgedate}, Message: {nudge.message}, Type: {nudge.type}, Status: {nudge.status}{Colors.ENDC}")
                elif nudge.sentiment == 0:
                    print(f"{Colors.YELLOW}Nudge Id: {nudge.id}, Name: {nudge.name}, Nudge Date: {nudge.nudgedate}, Message: {nudge.message}, Type: {nudge.type}, Status: {nudge.status}{Colors.ENDC}") 
                elif nudge.sentiment == 1:
                    print(f"{Colors.GREEN}Nudge Id: {nudge.id}, Name: {nudge.name}, Nudge Date: {nudge.nudgedate}, Message: {nudge.message}, Type: {nudge.type}, Status: {nudge.status}{Colors.ENDC}")
            print("**********************************************************")

        return 0
    def create_expense_category(self, category_name: str, category_description : str):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", (category_name, category_description))

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def create_expenses(self, expense: Expense):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = """
                INSERT INTO user_expense (name, amount, savedamount, settledamount, duedate, userid, categoryid, frequencyid, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                #db.insert_data(query, (expense.name, expense.amount, expense.savedamount, expense.settledamount, expense.duedate.to_pydatetime(), expense.userid, expense.categoryid, expense.frequencyid, expense.status))
                db.insert_data(query, (expense.name, expense.amount, expense.savedamount, expense.settledamount, expense.duedate, expense.userid, expense.categoryid, expense.frequencyid, expense.status))

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def create_income(self, amount:int, record_date: datetime, user_id:int=1):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = """
                INSERT INTO user_income (amount,record_date, userid)
                VALUES (?, ?, ?, ?)
                """
                db.insert_data(query, (amount, record_date,user_id))

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def update_expense(self, obj : Expense):
        try:
            print(f"Updating Expense ID: {obj.id} with Amount: {obj.amount}, Saved Amount: {obj.savedamount}, Settled Amount: {obj.settledamount}, Category ID: {obj.categoryid}, Status: {obj.status}, Due Date: {obj.duedate} ")
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = """
                UPDATE user_expense
                SET 
                name = ?,
                amount = ?
                ,savedamount = ?
                ,settledamount = ?
                ,duedate = ?
                ,categoryid = ?
                ,status = ?
                WHERE id = ? AND userid = ?
                """
                #print(f"query: {query}")
                db.execute_query(query, (obj.name, obj.amount, obj.savedamount, obj.settledamount, obj.duedate, obj.categoryid, obj.status, obj.id, self.userid))

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def update_savedamount(self, expense_id: int, new_savedamount: int):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = """
                UPDATE user_expense
                SET savedamount = savedamount + ?
                WHERE id = ? AND userid = ?
                """
                #print(f"query: {query}")
                db.execute_query(query, (new_savedamount, expense_id, self.userid))

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def update_settledamount(self, expense_id: int, new_settledamount: int):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = """
                UPDATE user_expense
                SET settledamount = settledamount + ?
                WHERE id = ? AND userid = ?
                """
                #print(f"query: {query}")
                db.execute_query(query, (new_settledamount, expense_id, self.userid))

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def create_table(self, table_schema: str):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                db.create_table(table_schema)

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def drop_table(self, table_name: str):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = f"DROP TABLE IF EXISTS {table_name}"
                #print(f"query: {query}")
                db.execute_query(query)

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    def upload_expense(self, filename: str):
        try:
            # to be implemented
            df = pd.read_excel(filename)
            #print(df)
            # --- Using iterrows() ---
            for index, row in df.iterrows():
                #print(f"Row Index: {index}, {row['name']}, {row['amount']}, {row['savedamount']}, {row['settledamount']}, {row['duedate']}, {row['userid']}, {row['categoryid']}, {row['frequencyid']}, {row['status']}")
                expense = Expense(0, row['name'], row['amount'], row['savedamount'], row['settledamount'], row['duedate'], row['userid'], row['categoryid'], row['frequencyid'], row['status'])
                self.create_expenses(expense)
        except Exception as e:
            print("--- Full Traceback ---")
            traceback.print_exc() 
            print("----------------------")
    def clear_table(self, table_name: str):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = f"DELETE FROM {table_name} WHERE userid = ?"
                #print(f"query: {query}")
                db.execute_query(query, (self.userid,))

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
        except Exception as e:
            print("--- Full Traceback ---")
            traceback.print_exc() 
            print("----------------------")