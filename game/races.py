import random
from game.database import connect
from game.player import reset_energy_if_new_day

AI_RACERS = [
    {"name": "Kaito", "car": "Civic EG", "rating": 230},
    {"name": "Zero", "car": "AE86", "rating": 260},
    {"name": "Redline", "car": "Silvia S13", "rating": 300},
    {"name": "Ghost", "car": "RX-7 FC", "rating": 340},
]


def race_ai(username):
    reset_energy_if_new_day(username)

    db = connect()
    cur = db.cursor()

    player = cur.execute(
        "SELECT money, reputation, energy, race_bonus FROM players WHERE username = ?",
        (username,)
    ).fetchone()

    car = cur.execute("""
        SELECT horsepower, handling, grip, reliability, condition, oil, tires, engine_wear
        FROM cars WHERE owner = ?
    """, (username,)).fetchone()

    if not player or not car:
        db.close()
        return "No car found. Start your player first."

    money, reputation, energy, race_bonus = player

    if energy <= 0:
        db.close()
        return """
⚡ You are out of energy.

Come back tomorrow to race again.
Daily energy resets once per day.
"""

    ai = random.choice(AI_RACERS)

    horsepower, handling, grip, reliability, condition, oil, tires, engine_wear = car

    player_score = (
        horsepower
        + handling
        + grip
        + reliability
        + random.randint(-40, 40)
        - (100 - condition)
        - (100 - oil)
        - (100 - tires)
        - engine_wear
    )

    ai_score = ai["rating"] + random.randint(-35, 35)

    tire_loss = random.randint(3, 8)
    oil_loss = random.randint(2, 6)
    engine_damage = random.randint(1, 4)
    condition_loss = random.randint(2, 6)

    cur.execute(
        "UPDATE players SET energy = energy - 1 WHERE username = ?",
        (username,)
    )

    cur.execute("""
        UPDATE cars
        SET tires = MAX(tires - ?, 0),
            oil = MAX(oil - ?, 0),
            engine_wear = engine_wear + ?,
            condition = MAX(condition - ?, 0)
        WHERE owner = ?
    """, (tire_loss, oil_loss, engine_damage, condition_loss, username))

    if player_score >= ai_score:
        base_payout = random.randint(700, 1600)
        bonus_amount = int(base_payout * (race_bonus / 100))
        payout = base_payout + bonus_amount
        rep_gain = random.randint(8, 22)

        cur.execute(
            "UPDATE players SET money = money + ?, reputation = reputation + ? WHERE username = ?",
            (payout, rep_gain, username)
        )

        result = f"""
🏁 AI Race Result

Opponent: {ai['name']}
Opponent Car: {ai['car']}

You won.

Earned:
Base Payout: ${base_payout}
Garage Bonus: +${bonus_amount}
Total: ${payout}
+{rep_gain} Reputation

Energy:
-1 Energy

Wear:
Tires -{tire_loss}%
Oil -{oil_loss}%
Engine Wear +{engine_damage}%
Condition -{condition_loss}%
"""
    else:
        rep_gain = random.randint(2, 6)

        cur.execute(
            "UPDATE players SET reputation = reputation + ? WHERE username = ?",
            (rep_gain, username)
        )

        result = f"""
🏁 AI Race Result

Opponent: {ai['name']}
Opponent Car: {ai['car']}

You lost.

Earned:
+{rep_gain} Reputation

Energy:
-1 Energy

Wear:
Tires -{tire_loss}%
Oil -{oil_loss}%
Engine Wear +{engine_damage}%
Condition -{condition_loss}%
"""

    db.commit()
    db.close()

    return result
