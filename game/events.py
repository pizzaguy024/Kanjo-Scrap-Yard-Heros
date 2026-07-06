import random
from game.database import connect

EVENTS = [
    {
        "name": "Heavy Rain",
        "text": "🌧 Heavy rain hits the expressway. Grip feels sketchy tonight.",
        "money": 0,
        "rep": 5,
    },
    {
        "name": "Low Oil",
        "text": "🛢 Your oil light flickers on. Engine wear increased.",
        "engine_wear": 8,
    },
    {
        "name": "Blown Tire",
        "text": "🛞 You hit debris near the docks. Tire condition dropped.",
        "tires": -25,
    },
    {
        "name": "Lucky Junkyard Find",
        "text": "🔩 You found a usable intake in the scrap pile.",
        "money": 450,
        "rep": 8,
    },
    {
        "name": "Police Crackdown",
        "text": "🚔 Police are heavy tonight. You kept it lowkey and earned street respect.",
        "money": -150,
        "rep": 15,
    },
    {
        "name": "Street Festival",
        "text": "🎌 The streets are packed. Your car gets noticed.",
        "rep": 20,
    },
]


def run_daily_event(username):
    db = connect()
    cur = db.cursor()

    player = cur.execute(
        "SELECT username FROM players WHERE username = ?",
        (username,)
    ).fetchone()

    if not player:
        db.close()
        return "No player found."

    event = random.choice(EVENTS)

    money_change = event.get("money", 0)
    rep_change = event.get("rep", 0)
    engine_wear = event.get("engine_wear", 0)
    tire_change = event.get("tires", 0)

    cur.execute("""
        UPDATE players
        SET money = MAX(money + ?, 0),
            reputation = reputation + ?
        WHERE username = ?
    """, (money_change, rep_change, username))

    cur.execute("""
        UPDATE cars
        SET engine_wear = engine_wear + ?,
            tires = MAX(tires + ?, 0)
        WHERE owner = ?
    """, (engine_wear, tire_change, username))

    db.commit()
    db.close()

    reward_text = ""

    if money_change > 0:
        reward_text += f"\nMoney: +${money_change}"
    elif money_change < 0:
        reward_text += f"\nMoney: -${abs(money_change)}"

    if rep_change > 0:
        reward_text += f"\nReputation: +{rep_change}"

    if engine_wear > 0:
        reward_text += f"\nEngine Wear: +{engine_wear}%"

    if tire_change < 0:
        reward_text += f"\nTires: {tire_change}%"

    return f"""
📅 Daily Event: {event['name']}

{event['text']}
{reward_text}
"""
