import random

STARTER_CARS = [
    {
        "name": "1992 Honda Civic Si",
        "rarity": "Common",
        "horsepower": 125,
        "handling": 65,
        "grip": 60,
        "reliability": 80,
    },
    {
        "name": "1995 Acura Integra GS-R",
        "rarity": "Common",
        "horsepower": 170,
        "handling": 70,
        "grip": 65,
        "reliability": 78,
    },
    {
        "name": "1989 Mazda Miata NA",
        "rarity": "Common",
        "horsepower": 116,
        "handling": 82,
        "grip": 68,
        "reliability": 75,
    },
    {
        "name": "1991 Nissan 240SX",
        "rarity": "Common",
        "horsepower": 155,
        "handling": 72,
        "grip": 62,
        "reliability": 70,
    },
    {
        "name": "1986 Toyota AE86",
        "rarity": "Rare",
        "horsepower": 128,
        "handling": 85,
        "grip": 70,
        "reliability": 82,
    },
    {
        "name": "1997 Honda Civic Type R EK9",
        "rarity": "Very Rare",
        "horsepower": 182,
        "handling": 88,
        "grip": 78,
        "reliability": 85,
    },
]


def random_starter_car():
    return random.choice(STARTER_CARS)
