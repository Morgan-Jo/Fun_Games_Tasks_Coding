# 🕵️‍♂️ The SQL Data Heist: Forensic Investigation

## 🚨 The Situation

At 02:14 AM on Saturday, a secure server was accessed, and 500GB of proprietary data was exfiltrated. The CEO has given you access to the internal logs. Your mission is to identify the **single employee** responsible for the breach.

## 🛠 Skills Demonstrated

This project showcases advanced SQL techniques used in real-world data auditing:
- **Window Functions**: Using `LEAD()` and `LAG()` to track sequential movement through physical rooms.
- **Common Table Expressions (CTEs)**: Organizing complex multi-step logic into readable blocks.
- **Temporal Analysis**: Querying timestamps to find "After-Hours" anomalies.
- **Aggregations & Filtering**: Finding users whose behavior deviates $3\sigma$ from the departmental mean.

## 🔎 The Investigation Path

To find the mole, you must solve three "Cases":
1. **The Midnight Badge**: Find everyone who entered the building between 12:00 AM and 04:00 AM on the day of the leak.
2. **The Unauthorized Access**: Cross-reference those employees with the room_access table to see who entered the Server Vault despite not being in the IT department.
3. **The Final Evidence**: Look for the employee who had a file_transfer_size greater than the average of their last 30 days of activity.

## 📁 Project Sturcutre
```txt
sql_data_heist/
├── db/
│   ├── schema.sql          # DDL: Defines tables (employees, logs, access)
│   ├── seed_data.py        # Python script to generate "normal" vs "mole" data
│   └── data_heist.db       # The SQLite database (Git-ignored, generated locally)
├── notebooks/
│   └── investigation.ipynb  # Narrative data storytelling & visualization
├── queries/
│   ├── clues.sql           # Step-by-step SQL hints (Filter -> Join -> Window)
│   └── solution.sql        # The "Smoking Gun" multi-CTE query
├── src/
│   └── utils.py            # Shared functions (DB connections, formatting)
├── main.py                 # The interactive Terminal Investigation interface
├── requirements.txt        # Pinned dependencies (pandas, matplotlib, etc.)
└── README.md               # Case overview, setup, and instructionssql_data_heist/
```

## 🚀 How to use
```bash
# Create and activate a clean environment
python -m venv heist_env
source heist_env/bin/activate  # On Windows: heist_env\Scripts\activate

# Install the forensic toolkit
pip install -r requirements.txt

# Seed the crime scene
python db/seed_data.py

# Begin the investigation
python main.py
```

## ✍️ Author
Morgan J. Tonner

## ⚠️ Disclaimer
🕵️‍♂️ Fictional Context & Ethics
This project is a gamified educational tool designed to teach SQL and data forensics.

- **Fictional Scenario**: All employee names, company data, and "Project X" blueprints are entirely fictional. Any resemblance to actual persons, living or dead, or actual corporate events is purely coincidental.
- **Synthetic Data**: The data used in this project is generated programmatically. No real PII (Personally Identifiable Information) or sensitive corporate logs were used in the creation of this database.
- **Non-Malicious Intent**: This project does not teach "hacking." It focuses on defensive analysis and audit trail auditing from the perspective of a data analyst.