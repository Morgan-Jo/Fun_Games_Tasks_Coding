import sqlite3
import os

def init_db():
    conn = sqlite3.connect(':memory:') # Fresh DB for every run
    cursor = conn.cursor()
    # Read and execute the SQL seed file
    sql_script = """
    CREATE TABLE classes (class_id INT, class_name TEXT);
    CREATE TABLE monsters (id INT, name TEXT, class_id INT);
    CREATE TABLE resistances (class_id INT, weakness_type TEXT);
    CREATE TABLE equipment (item_name TEXT, damage_type TEXT);

    INSERT INTO classes VALUES (1, 'Undead'), (2, 'Beast');
    INSERT INTO monsters VALUES (1, 'Skeleton King', 1), (2, 'Dire Wolf', 2);
    INSERT INTO resistances VALUES (1, 'Holy'), (2, 'Fire');
    INSERT INTO equipment VALUES ('Sun Sword', 'Holy'), ('Torch', 'Fire');
    """
    cursor.executescript(sql_script)
    return conn

def game_loop():
    conn = init_db()
    cursor = conn.cursor()
    
    print("--- WELCOME TO THE SQL DUNGEON ---")
    print("A 'Skeleton King' (Undead) appears! You must find a weapon")
    print("in your 'equipment' table that matches his 'weakness_type'.")
    print("-" * 40)
    print("PROMPT: Write a JOIN query to find the 'item_name' that kills the 'Skeleton King'.")
    
    # Expected Query: 
    # SELECT e.item_name FROM equipment e 
    # JOIN resistances r ON e.damage_type = r.weakness_type
    # JOIN monsters m ON m.class_id = r.class_id 
    # WHERE m.name = 'Skeleton King'

    user_query = input("\nSQL> ")
    
    try:
        cursor.execute(user_query)
        result = cursor.fetchone()
        
        if result and 'Sun Sword' in result:
            print("\n[SUCCESS] You strike with the Sun Sword! The Undead crumbles.")
        else:
            print("\n[FAILURE] The query ran, but it didn't return the right weapon!")
    except Exception as e:
        print(f"\n[SYNTAX ERROR] {e}")

if __name__ == "__main__":
    game_loop()