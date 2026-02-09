-- Employee Directory
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    clearance_level INT,
    hire_date DATE
);

-- Physical Security Logs
CREATE TABLE badge_access (
    access_id INTEGER PRIMARY KEY,
    emp_id INT,
    room_id TEXT,
    entry_time TIMESTAMP,
    exit_time TIMESTAMP,
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
);

-- Network Activity Logs
CREATE TABLE network_logs (
    log_id INTEGER PRIMARY KEY,
    emp_id INT,
    action TEXT, -- 'LOGIN', 'FILE_DOWNLOAD', 'LOGOUT'
    file_name TEXT,
    file_size_mb FLOAT,
    timestamp TIMESTAMP,
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
);