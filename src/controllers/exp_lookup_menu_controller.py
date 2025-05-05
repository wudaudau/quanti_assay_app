"""
"""

from src.controllers.exp_menu_controller import show_menu_title, ask_a_menu_choice

from src.controllers.exp_lookup_controller import lookup_experiments_flow


def exp_lookup_menu():
    """
    Display the Experiment Lookup menu.
    """
    print("\nWhat do you want to do?")
    print("1. Lookup Last 15 Experiments") # TODO: Make this a "Lookup menu"
    print("2. Lookup All Experiments")
    print()
    print("3. Back to Experiment Menu")
    print("4. Back to Main Menu")
    print()

def exp_lookup_menu_flow(db_path):
    """
    Experiment Lookup menu flow.
    The parent flow is exp_menu_flow().
    This function will display the Experiment Lookup menu and handle user input.
    Returns the result of the Experiment Lookup menu.
    """
    while True:
        show_menu_title("Experiment Lookup Menu")

        exp_lookup_menu()
        choice = ask_a_menu_choice(["1", "2", "3", "4"])

        if choice == "1":
            result = lookup_experiments_flow(db_path, 15) # TODO: Refactor this to return a result
        elif choice == "2":
            result = lookup_experiments_flow(db_path)
        elif choice == "3":
            result = "exp menu"
            print("Returning to Experiment Menu...")
        elif choice == "4":
            result = "main menu"
            print("Returning to Main Menu...")

        # Handle the result of the exp lookup menu
        if result == "exp lookup menu":
            continue
        elif result == "exp menu":
            return result
        elif result == "main menu":
            return result