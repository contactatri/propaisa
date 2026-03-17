import sqlite3

class SQLiteManager:
    """
    A Python class for managing SQLite database connections and operations.
    """
    def __init__(self, db_file):
        """Initialize with the database file name."""
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open a database connection and create a cursor using a context manager."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            # Optional: use row_factory to access results as dictionaries
            self.conn.row_factory = sqlite3.Row 
            self.cursor = self.conn.cursor()
            return self

        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            # Propagate the exception so the 'with' block fails if connection fails
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection automatically when exiting the context."""
        if self.conn:
            if exc_type is None:
                # Commit changes if no exceptions occurred within the 'with' block
                self.conn.commit()
            else:
                # Rollback changes if an exception occurred
                self.conn.rollback()
            self.conn.close()

    def execute_query(self, query, parameters=()):
        """Execute a single query with optional parameters."""
        self.cursor.execute(query, parameters)
        return self.cursor

    def fetch_all(self, query, parameters=()):
        """Execute a query and fetch all results."""
        self.execute_query(query, parameters)
        return self.cursor.fetchall()

    def fetch_one(self, query, parameters=()):
        """Execute a query and fetch one result."""
        self.execute_query(query, parameters)
        return self.cursor.fetchone()

    def create_table(self, table_schema):
        """Create a table using a provided SQL schema string."""
        self.execute_query(table_schema)
        print(f"Table created/ensured: {table_schema.split()[2]}")

    def insert_data(self, query, data):
        """Insert a single row of data."""
        self.execute_query(query, data)
        return self.cursor.lastrowid
