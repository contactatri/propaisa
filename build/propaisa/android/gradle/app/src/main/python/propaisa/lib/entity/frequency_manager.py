import sqlite3
from typing import Dict, Any, ClassVar
from lib.entity.sqlitemanager import SQLiteManager 
class Frequency:
    def __init__(self, id, name):
        self.id = id
        self.name = name
class FrequencyManager:
    """
    A class to set up the SQLite database with required tables for frequency management.
    """
    def __init__(self, db_file):
        self.db_file = db_file
        self.frequencies = []
        try:
            # Connect to the database and use the connection as a context manager
            with SQLiteManager(self.db_file) as db:
                #query = "SELECT id,name FROM expense_frequency WHERE id > ?"
                query = "SELECT id,name FROM expense_frequency"
                rows = db.fetch_all(query)
                if rows:
                    #print(f"Students older than {min_age}:")                    
                    for row in rows:
                        frequency = Frequency(row[0], row[1])
                        self.frequencies.append(frequency)
                        #print(f"Name: {frequency.name}, Id: {frequency.id}")

                else:
                    print(f"No records found.")

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")

        