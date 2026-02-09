import sqlite3
import random
from datetime import datetime, timedelta

def seed_database():
    conn = sqlite3.connect('db/data_heist.db')
    cursor = conn.cursor()

    # 1. Create Schema
    cursor.executescript('''
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS badge_access;
        DROP TABLE IF EXISTS network_logs;

        CREATE TABLE employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            clearance_level INT
        );

        CREATE TABLE badge_access (
            access_id INTEGER PRIMARY KEY,
            emp_id INT,
            room_id TEXT,
            entry_time TIMESTAMP,
            exit_time TIMESTAMP
        );

        CREATE TABLE network_logs (
            log_id INTEGER PRIMARY KEY,
            emp_id INT,
            action TEXT,
            file_name TEXT,
            file_size_mb FLOAT,
            timestamp TIMESTAMP
        );
    ''')

    # 2. Generate 50 Employees
    depts = ['IT', 'HR', 'Finance', 'Sales', 'Engineering']
    names = ['Alice Smith', 'Bob Jones', 'Charlie Brown', 'Diana Prince', 'Edward Norton', 
             'Fiona Gallagher', 'George Costanza', 'Hannah Abbott', 'Ian Wright', 'Thomas Miller']
    # Add more random names to reach 50...
    
    employee_pool = []
    for i in range(1, 51):
        name = random.choice(names) + f" {i}"
        dept = random.choice(depts)
        clearance = random.randint(1, 4)
        cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?)", (i, name, dept, clearance))
        employee_pool.append((i, dept))

    # 3. Generate "Normal" History (The Baseline)
    # 30 days of data
    start_date = datetime(2026, 1, 7)
    
    for emp_id, dept in employee_pool:
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            
            # Normal working hours: 08:00 - 18:00
            entry = current_date.replace(hour=random.randint(8, 10), minute=random.randint(0, 59))
            exit = entry + timedelta(hours=random.randint(7, 9))
            
            cursor.execute("INSERT INTO badge_access (emp_id, room_id, entry_time, exit_time) VALUES (?, ?, ?, ?)",
                           (emp_id, 'Main Lobby', entry, exit))
            
            # Normal network activity (Small files)
            cursor.execute("INSERT INTO network_logs (emp_id, action, file_name, file_size_mb, timestamp) VALUES (?, ?, ?, ?, ?)",
                           (emp_id, 'FILE_DOWNLOAD', f'doc_{day}.pdf', random.uniform(1.0, 50.0), entry + timedelta(hours=2)))

    # 4. INJECT THE MOLE (The Anomaly)
    # Let's pick Employee 42 (Thomas Miller in Sales)
    mole_id = 42
    leak_date = datetime(2026, 2, 7, 2, 14, 0) # The night of the heist
    
    # The Suspect enters the building at 2 AM
    cursor.execute("INSERT INTO badge_access (emp_id, room_id, entry_time, exit_time) VALUES (?, ?, ?, ?)",
                   (mole_id, 'Main Lobby', leak_date, leak_date + timedelta(minutes=120)))
    
    # The Suspect enters the Server Vault (They shouldn't be there!)
    cursor.execute("INSERT INTO badge_access (emp_id, room_id, entry_time, exit_time) VALUES (?, ?, ?, ?)",
                   (mole_id, 'Server Vault', leak_date + timedelta(minutes=10), leak_date + timedelta(minutes=60)))
    
    # The massive exfiltration (500,000 MB)
    cursor.execute("INSERT INTO network_logs (emp_id, action, file_name, file_size_mb, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (mole_id, 'FILE_DOWNLOAD', 'PROJECT_X_BLUEPRINTS.zip', 500000.0, leak_date + timedelta(minutes=15)))

    conn.commit()
    conn.close()
    print("Database seeded successfully. The mole is hidden...")

if __name__ == "__main__":
    seed_database()