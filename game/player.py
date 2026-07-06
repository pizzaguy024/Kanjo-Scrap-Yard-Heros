from game.database import connect
from game.cars import random_starter_car


def create_player(username):
    db = connect()
    cur = db.cursor()

    existing = cur.execute(
        "SELECT username FROM players WHERE username = ?",
        (username,)
    ).fetchone()

    if existing:
        db.close()
        return "You already have a profile."

    car = random_starter_car()

    cur.execute(
        "INSERT INTO players (username, money, reputation, garage_level) VALUES (?, ?, ?, ?)",
        (username, 500, 0, 1)
    )

    cur.execute("""
        INSERT INTO cars (
            owner, name, rarity, horsepower, handling, grip, reliability,
            condition, oil, tires, engine_wear, upgrade_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        car["name"],
        car["rarity"],
        car["horsepower"],
        car["handling"],
        car["grip"],
        car["reliability"],
        75,
        100,
        100,
        0,
        0
    ))

    db.commit()
    db.close()

    return f"""
🏚️ Welcome to the Scrap Yard.

You found:

{car['name']}
Rarity: {car['rarity']}

Money: $500
Reputation: 0

Build it. Race it. Survive it.
"""


def get_player_profile(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute(
        "SELECT money, reputation, garage_level FROM players WHERE username = ?",
        (username,)
    ).fetchone()

    if not player:
        db.close()
        return "No profile found. Choose Start New Player first."

    car = cur.execute(
        "SELECT name, rarity, horsepower, handling, grip, reliability, condition FROM cars WHERE owner = ?",
        (username,)
    ).fetchone()

    db.close()

    money, rep, garage_level = player

    return f"""
👤 Driver: {username}

Money: ${money}
Reputation: {rep}
Garage Level: {garage_level}

Current Car:
{car[0]}
Rarity: {car[1]}
Horsepower: {car[2]}
Handling: {car[3]}
Grip: {car[4]}
Reliability: {car[5]}
Condition: {car[6]}%
"""
