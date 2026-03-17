import sqlite3
from typing import Dict, Any, ClassVar
from lib.sqlitemanager import SQLiteManager 
class ExpenseCategory:
    def __init__(self, id, name):
        self.id = id
        self.name = name
class ExpenseCategoryManager:
    """
    A class to set up the SQLite database with required tables for expense category management.
    """
    def __init__(self, db_file):
        self.db_file = db_file
        self.expense_categories = []
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                #query = "SELECT id,name FROM expense_frequency WHERE id > ?"
                query = "SELECT id,name FROM expense_category"
                rows = db.fetch_all(query)
                if rows:                
                    for row in rows:
                        expense_category = ExpenseCategory(row[0], row[1])
                        self.expense_categories.append(expense_category)
                        #print(f"Name: {expense_category.name}, Id: {expense_category.id}")

                else:
                    print(f"No records found.")

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")

        