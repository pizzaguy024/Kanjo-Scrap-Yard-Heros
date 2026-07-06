from game.database import connect


def show_garage(username):
    db = connect()
    cur = db.cursor()

    car = cur.execute("""
        SELECT name, rarity, horsepower, handling, grip, reliability,
               condition, oil, tires, engine_wear, upgrade_level
        FROM cars WHERE owner = ?
    """, (username,)).fetchone()

    if not car:
        db.close()
        return "No garage found."

    db.close()

    return f"""
🔧 Garage

Car: {car[0]}
Rarity: {car[1]}

Performance:
Horsepower: {car[2]}
Handling: {car[3]}
Grip: {car[4]}
Reliability: {car[5]}

Condition:
Body Condition: {car[6]}%
Oil: {car[7]}%
Tires: {car[8]}%
Engine Wear: {car[9]}%

Upgrade Level: {car[10]}
"""


def repair_car(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute(
        "SELECT money FROM players WHERE username = ?",
        (username,)
    ).fetchone()

    if not player:
        db.close()
        return "No player found."

    repair_cost = 500

    if player[0] < repair_cost:
        db.close()
        return f"You need ${repair_cost} to repair your car."

    cur.execute(
        "UPDATE players SET money = money - ? WHERE username = ?",
        (repair_cost, username)
    )

    cur.execute("""
        UPDATE cars
        SET condition = 100,
            oil = 100,
            tires = 100,
            engine_wear = 0
        WHERE owner = ?
    """, (username,))

    db.commit()
    db.close()

    return f"🔧 Full repair complete. You spent ${repair_cost}."


def upgrade_car(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute(
        "SELECT money FROM players WHERE username = ?",
        (username,)
    ).fetchone()

    car = cur.execute(
        "SELECT upgrade_level FROM cars WHERE owner = ?",
        (username,)
    ).fetchone()

    if not player or not car:
        db.close()
        return "No car found."

    upgrade_level = car[0]
    cost = 750 + upgrade_level * 500

    if player[0] < cost:
        db.close()
        return f"You need ${cost} for the next upgrade."

    cur.execute(
        "UPDATE players SET money = money - ? WHERE username = ?",
        (cost, username)
    )

    cur.execute("""
        UPDATE cars
        SET horsepower = horsepower + 15,
            handling = handling + 3,
            grip = grip + 3,
            reliability = reliability + 2,
            upgrade_level = upgrade_level + 1
        WHERE owner = ?
    """, (username,))

    db.commit()
    db.close()

    return f"⚙️ Upgrade installed. You spent ${cost}."
