import sqlite3

DB_NAME = "kanjo.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        money INTEGER,
        reputation INTEGER,
        garage_level INTEGER,
        energy INTEGER DEFAULT 10,
        max_energy INTEGER DEFAULT 10,
        last_energy_reset TEXT,
        last_daily_event TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT,
        name TEXT,
        rarity TEXT,
        horsepower INTEGER,
        handling INTEGER,
        grip INTEGER,
        reliability INTEGER,
        condition INTEGER,
        oil INTEGER,
        tires INTEGER,
        engine_wear INTEGER,
        upgrade_level INTEGER
    )
    """)

    # Adds new columns if your old database already exists
    for column, column_type in [
        ("energy", "INTEGER DEFAULT 10"),
        ("max_energy", "INTEGER DEFAULT 10"),
        ("last_energy_reset", "TEXT"),
        ("last_daily_event", "TEXT"),
    ]:
        try:
            cur.execute(f"ALTER TABLE players ADD COLUMN {column} {column_type}")
        except sqlite3.OperationalError:
            pass

    db.commit()
    db.close()
