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
        garage_level INTEGER
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

    db.commit()
    db.close()
