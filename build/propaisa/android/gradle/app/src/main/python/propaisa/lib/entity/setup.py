from lib.entity.sqlitemanager import SQLiteManager 
import sqlite3
class Setup:
    """
    A class to set up the SQLite database with required tables.
    """
    def __init__(self, db_file):
        self.db_file = db_file
    def clear_table(self, tablename : str):
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                query = f"delete from {tablename}"
                db.execute_query(query)

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
    
    def initialize_database(self):
        """Initialize the database and create necessary tables."""
        with SQLiteManager(self.db_file) as db:
            # Define table schemas
            user_table_schema = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """

            expense_category_table_schema = """
            CREATE TABLE IF NOT EXISTS expense_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """

            expense_frequency_table_schema = """
            CREATE TABLE IF NOT EXISTS expense_frequency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """

            # Status 0 for active, 1 for completed, -1 for overdue
            user_expense_table_schema = """
            CREATE TABLE IF NOT EXISTS user_expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                savedamount INTEGER NOT NULL,
                settledamount INTEGER NOT NULL,
                userid INTEGER NOT NULL,
                categoryid INTEGER NOT NULL,
                frequencyid INTEGER NOT NULL,
                status INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duedate TIMESTAMP,
                FOREIGN KEY(userid) REFERENCES users(id),
                FOREIGN KEY(categoryid) REFERENCES expense_category(id),
                FOREIGN KEY(frequencyid) REFERENCES expense_frequency(id)
            );
            """
            user_txn_table_schema = """
            CREATE TABLE IF NOT EXISTS user_txn (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount INTEGER NOT NULL,
                userid INTEGER NOT NULL,
                userexpenseid INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(userid) REFERENCES users(id),
                FOREIGN KEY(userexpenseid) REFERENCES user_expense(id)
            );
            """
            user_income_table_schema = """
            CREATE TABLE IF NOT EXISTS user_income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount INTEGER NOT NULL,
                userid INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(userid) REFERENCES users(id)
            );
            """

            # Create tables
            db.create_table(user_table_schema)
            db.create_table(expense_category_table_schema)
            db.create_table(expense_frequency_table_schema)
            db.create_table(user_expense_table_schema)
            db.create_table(user_txn_table_schema)
            db.create_table(user_income_table_schema)

            print("Database initialized with required tables.")
            # Insert initial data into users table
            db.insert_data("INSERT INTO users (username, email) VALUES (?, ?)", ('a.kuppuswami', 'a.kuppuswami@gmail.com'))
            db.insert_data("INSERT INTO users (username, email) VALUES (?, ?)", ('n.kuppuswami', 'n.kuppuswami@gmail.com'))
            # Insert initial data into expense_frequency table
            db.insert_data("INSERT INTO expense_frequency (name, description) VALUES (?, ?)", ('daily', 'daily expenses'))
            db.insert_data("INSERT INTO expense_frequency (name, description) VALUES (?, ?)", ('fortnightly', 'fortnightly expenses'))
            db.insert_data("INSERT INTO expense_frequency (name, description) VALUES (?, ?)", ('monthly', 'monthly expenses'))
            db.insert_data("INSERT INTO expense_frequency (name, description) VALUES (?, ?)", ('quarterly', 'quarterly expenses'))
            db.insert_data("INSERT INTO expense_frequency (name, description) VALUES (?, ?)", ('half-yearly', 'half-yearly expenses'))
            db.insert_data("INSERT INTO expense_frequency (name, description) VALUES (?, ?)", ('yearly', 'yearly expenses'))
            # Insert initial data into expense_category table
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Rent/Mortgage', 'Rent or mortgage payments'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Utilities', 'Electricity, water, gas, internet, etc.'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Groceries', 'Food and household supplies'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Transportation', 'Public transport, fuel, car maintenance'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Dining Out', 'Restaurants, cafes, takeout'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Entertainment', 'Movies, concerts, hobbies'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Healthcare', 'Medical expenses, insurance'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Education', 'Tuition, books, courses'))
            db.insert_data("INSERT INTO expense_category (name, description) VALUES (?, ?)", ('Principle/Interest', 'Principle/Interest paid to lenders')) 

