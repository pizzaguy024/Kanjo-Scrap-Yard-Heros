from game.database import init_db
from game.player import create_player, get_player_profile
from game.races import race_ai
from game.garage import show_garage, repair_car, upgrade_car, upgrade_garage
from game.events import run_daily_event


def menu():
    print("\n=== KANJO: SCRAP YARD HEROES ===")
    print("1. Start New Player")
    print("2. Profile")
    print("3. Garage")
    print("4. Race AI")
    print("5. Repair Car")
    print("6. Upgrade Car")
    print("7. Daily Event")
    print("8. Upgrade Garage")
    print("9. Quit")


def main():
    init_db()

    username = input("Enter your player name: ").strip()

    while True:
        menu()
        choice = input("> ").strip()

        if choice == "1":
            print(create_player(username))
        elif choice == "2":
            print(get_player_profile(username))
        elif choice == "3":
            print(show_garage(username))
        elif choice == "4":
            print(race_ai(username))
        elif choice == "5":
            print(repair_car(username))
        elif choice == "6":
            print(upgrade_car(username))
        elif choice == "7":
            print(run_daily_event(username))
        elif choice == "8":
            print(upgrade_garage(username))
        elif choice == "9":
            print("Later, street runner.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
