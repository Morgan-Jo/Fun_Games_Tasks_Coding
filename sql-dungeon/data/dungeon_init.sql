-- Create Tables
CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY,
    class_name TEXT
);

CREATE TABLE monsters (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class_id INTEGER,
    hp INTEGER,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

CREATE TABLE resistances (
    class_id INTEGER,
    weakness_type TEXT,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

CREATE TABLE equipment (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT,
    damage_type TEXT,
    power INTEGER
);

-- Seed Data
INSERT INTO classes VALUES (1, 'Undead'), (2, 'Beast'), (3, 'Construct');
INSERT INTO monsters VALUES (1, 'Skeleton King', 1, 100), (2, 'Dire Wolf', 2, 50), (3, 'Steam Golem', 3, 200);
INSERT INTO resistances VALUES (1, 'Holy'), (2, 'Fire'), (3, 'Lightning');
INSERT INTO equipment VALUES (1, 'Sun Sword', 'Holy', 50), (2, 'Torch', 'Fire', 20), (3, 'Electric Mace', 'Lightning', 40);