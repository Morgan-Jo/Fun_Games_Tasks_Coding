import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional

class DatabaseHandler:
    """
    Utility class to manage SQLite connections and queries.
    Handles pathing automatically for Notebooks vs CLI.
    """
    
    def __init__(self, db_name: str = "data_heist.db"):
        # Automatically find the project root (where the .git or main.py lives)
        self.project_root = Path(__file__).parent.parent
        self.db_path = self.project_root / "db" / db_name

    def get_connection(self):
        """Returns a standard sqlite3 connection object."""
        try:
            conn = sqlite3.connect(self.db_path)
            # Enable foreign key support (important for data integrity)
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn
        except sqlite3.Error as e:
            print(f"❌ Database connection failed: {e}")
            return None

    def query_to_dataframe(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        """
        Executes a query and returns a Pandas DataFrame.
        Perfect for the 'investigation.ipynb' notebook.
        """
        conn = self.get_connection()
        if conn:
            try:
                df = pd.read_sql_query(sql, conn, params=params)
                return df
            finally:
                conn.close()
        return pd.DataFrame()

    def run_command(self, sql: str, params: tuple = ()):
        """
        Executes a command (INSERT, UPDATE, DELETE) and commits.
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
            except sqlite3.Error as e:
                print(f"❌ Command failed: {e}")
            finally:
                conn.close()