from game.database import connect


GARAGE_LEVELS = {
    1: {
        "cost": 0,
        "max_energy": 10,
        "repair_discount": 0,
        "race_bonus": 0,
        "car_slots": 1,
    },
    2: {
        "cost": 2500,
        "max_energy": 12,
        "repair_discount": 5,
        "race_bonus": 3,
        "car_slots": 2,
    },
    3: {
        "cost": 6000,
        "max_energy": 14,
        "repair_discount": 10,
        "race_bonus": 5,
        "car_slots": 3,
    },
    4: {
        "cost": 12000,
        "max_energy": 16,
        "repair_discount": 15,
        "race_bonus": 8,
        "car_slots": 4,
    },
    5: {
        "cost": 25000,
        "max_energy": 18,
        "repair_discount": 20,
        "race_bonus": 10,
        "car_slots": 5,
    },
}


def show_garage(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT garage_level, max_energy, repair_discount, race_bonus, car_slots
        FROM players WHERE username = ?
    """, (username,)).fetchone()

    car = cur.execute("""
        SELECT name, rarity, horsepower, handling, grip, reliability,
               condition, oil, tires, engine_wear, upgrade_level
        FROM cars WHERE owner = ?
    """, (username,)).fetchone()

    if not player or not car:
        db.close()
        return "No garage found."

    db.close()

    garage_level, max_energy, repair_discount, race_bonus, car_slots = player

    next_level = garage_level + 1
    next_upgrade_text = ""

    if next_level in GARAGE_LEVELS:
        next_data = GARAGE_LEVELS[next_level]
        next_upgrade_text = f"""
Next Garage Upgrade:
Level {next_level}
Cost: ${next_data['cost']}
Max Energy: {next_data['max_energy']}
Repair Discount: {next_data['repair_discount']}%
Race Payout Bonus: {next_data['race_bonus']}%
Car Slots: {next_data['car_slots']}
"""
    else:
        next_upgrade_text = """
Garage is fully upgraded.
"""

    return f"""
🔧 Garage

Garage Level: {garage_level}
Max Energy: {max_energy}
Repair Discount: {repair_discount}%
Race Payout Bonus: {race_bonus}%
Car Slots: {car_slots}

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

{next_upgrade_text}
"""


def repair_car(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT money, repair_discount
        FROM players WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return "No player found."

    money, repair_discount = player

    base_repair_cost = 500
    discount_amount = int(base_repair_cost * (repair_discount / 100))
    repair_cost = base_repair_cost - discount_amount

    if money < repair_cost:
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

    return f"""
🔧 Full repair complete.

Base Cost: ${base_repair_cost}
Garage Discount: {repair_discount}%
Final Cost: ${repair_cost}
"""


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

    money = player[0]
    upgrade_level = car[0]
    cost = 750 + upgrade_level * 500

    if money < cost:
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


def upgrade_garage(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute("""
        SELECT money, garage_level
        FROM players WHERE username = ?
    """, (username,)).fetchone()

    if not player:
        db.close()
        return "No player found."

    money, garage_level = player
    next_level = garage_level + 1

    if next_level not in GARAGE_LEVELS:
        db.close()
        return "Your garage is already fully upgraded."

    upgrade_data = GARAGE_LEVELS[next_level]
    cost = upgrade_data["cost"]

    if money < cost:
        db.close()
        return f"""
You need ${cost} to upgrade to Garage Level {next_level}.

Current Money: ${money}
"""

    cur.execute("""
        UPDATE players
        SET money = money - ?,
            garage_level = ?,
            max_energy = ?,
            energy = ?,
            repair_discount = ?,
            race_bonus = ?,
            car_slots = ?
        WHERE username = ?
    """, (
        cost,
        next_level,
        upgrade_data["max_energy"],
        upgrade_data["max_energy"],
        upgrade_data["repair_discount"],
        upgrade_data["race_bonus"],
        upgrade_data["car_slots"],
        username
    ))

    db.commit()
    db.close()

    return f"""
🏚️ Garage Upgraded

New Garage Level: {next_level}
Cost: ${cost}

New Benefits:
Max Energy: {upgrade_data['max_energy']}
Repair Discount: {upgrade_data['repair_discount']}%
Race Payout Bonus: {upgrade_data['race_bonus']}%
Car Slots: {upgrade_data['car_slots']}
"""
