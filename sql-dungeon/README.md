# SQL Dungeon: The Relational Crawler

A terminal-based RPG where your primary weapon is the **Structured Query Language**. To defeat enemies and progress through the dungeon, you must perform joins, filter data, and calculate aggregations.

## 🛠 Tech Stack
- **Language:** Python 3.x
- **Database:** SQLite3
- **Skills:** Relational Algebra, Data Filtering, Subqueries.

## 🕹 How to Play
1. Run `python src/main.py`.
2. Read the scenario presented in the terminal.
3. Write the correct SQL query to "find a weakness" or "calculate gold."
4. If the query returns the correct result, you progress!

## 🧩 Schema Overview
The game uses a normalized database with four main tables:
- `monsters`: Basic stats for enemies.
- `classes`: Categorizes monsters (Undead, Beast, etc.).
- `resistances`: Maps classes to damage types (Fire, Holy, etc.).
- `equipment`: Items available in your inventory.

## 📁 Project Structure
```txt
sql-dungeon/
├── data/
│   └── dungeon_init.sql    # The raw SQL schema and seed data
├── src/
│   ├── main.py             # The Python game engine
│   └── database.py         # DB connection and logic
├── game_info.txt           # Overview for players
├── README.md               # Professional documentation
└── requirements.txt
```

## 📋 Requirements 
Python 3.9 or later

Your preferred editor - mine is VS Code

## 🚀 Run
1. Setup and Launch
    - Open terminal
    - Navigate to project folder
    - Run the game
    ```r
    python src/main.py
    ```
2. How to "Fight"
    - When the game starts, you will be presented with a Scenario. Instead of a "Battle" menu, you will see a prompt that looks like this: `SQL>`
    - The Goal: You need to write a SQL query that returns the exact value the game is looking for.
        - **Example Scenario:** A "Skeleton King" appears. He is an "Undead" class.
        - **Your Mission:** Find the name of the weapon in your `equipment` table that has the `damage_type` required to kill him.
3. Solving the Level
    - To win the encounter, you must perform a **JOIN**. The game logic is checking if your query result matches the "Winning Item."
4. Rules & Feedback
    - **Syntax Errors:** If you forget a comma or semicolon, the Python `sqlite3` engine will throw an error message. Read it carefully—it tells you exactly where your SQL is broken!
    - **Logical Errors:** If your query runs but returns the wrong item (e.g., you accidentally picked a "Torch" for a Water monster), the game will tell you your attack missed.
    - **Case Sensitivity:** In some SQL setups, 'Holy' is different from 'holy'. Always match the casing used in the setup script.
5. Quick Reference for Commands
    - If you get stuck, remember the schema you built:
        - **Tables:** `monsters`, `classes`, `resistances`, `equipment`
        - **Links:**
            - `monsters.class_id` = `classes.class_id`
            - `classes.class_id` = `resistances.class_id`
            - `resistances.weakness_type` = `equipment.damage_type`

## ✍️ Author
Morgan J. Tonner 

## ⚠️ Disclaimer
This project was intended solely for practice, learning, testing or portfolio use own. This game is for some coding fun.