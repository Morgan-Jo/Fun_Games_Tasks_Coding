import sqlite3
import pandas as pd
from db.seed_data import seed_database
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_investigation_query(query_title, sql_query):
    """Executes a query and displays the results in a clean format."""
    conn = sqlite3.connect('db/data_heist.db')
    print(f"\n--- {query_title} ---")
    try:
        df = pd.read_sql_query(sql_query, conn)
        if df.empty:
            print("No results found. The mole is still at large.")
        else:
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()

def main():
    # 1. Initialize the crime scene
    if not os.path.exists('db/data_heist.db'):
        print("Initializing forensic database...")
        seed_database()

    while True:
        print("\n" + "="*40)
        print("🕵️‍♂️ SQL DATA HEIST: INVESTIGATION CONSOLE")
        print("="*40)
        print("1. Run Clue #1: The Midnight Badge (Late Night Entry)")
        print("2. Run Clue #2: The Unauthorized Vault Access (Non-IT)")
        print("3. Run Clue #3: The Smoking Gun (Outlier Transfer Size)")
        print("4. Reset Database (Re-generate Evidence)")
        print("5. Exit Investigation")
        
        choice = input("\nSelect an action [1-5]: ")

        if choice == '1':
            sql = "SELECT e.name, e.department, b.entry_time FROM employees e JOIN badge_access b ON e.emp_id = b.emp_id WHERE time(b.entry_time) BETWEEN '00:00:00' AND '04:00:00';"
            run_investigation_query("LATE NIGHT ENTRIES", sql)
        
        elif choice == '2':
            sql = "SELECT e.name, e.department, b.room_id FROM employees e JOIN badge_access b ON e.emp_id = b.emp_id WHERE b.room_id = 'Server Vault' AND e.department != 'IT';"
            run_investigation_query("UNAUTHORIZED ROOM ACCESS", sql)
        
        elif choice == '3':
            sql = """
            WITH UserBaselines AS (
                SELECT emp_id, file_size_mb, AVG(file_size_mb) OVER(PARTITION BY emp_id) as avg_size
                FROM network_logs
            )
            SELECT e.name, nl.file_name, nl.file_size_mb, ub.avg_size
            FROM network_logs nl
            JOIN employees e ON nl.emp_id = e.emp_id
            JOIN UserBaselines ub ON nl.emp_id = ub.emp_id
            WHERE nl.file_size_mb > (ub.avg_size * 100);
            """
            run_investigation_query("ANOMALOUS FILE TRANSFERS", sql)

        elif choice == '4':
            seed_database()
            print("Database has been reset with new randomized data.")

        elif choice == '5':
            print("Exiting console. Case closed.")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()