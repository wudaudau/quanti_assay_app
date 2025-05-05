"""
"""

from src.controllers.controller_utils import show_menu_title, ask_a_menu_choice

from src.controllers.exp_logging_controller import log_experiment_flow_manually, log_experiment_flow_from_file


def exp_logging_menu():
    """
    Display the Experiment Logging menu.
    """
    print("\nWhat do you want to do?")
    print("1. Log Experiment manually")
    print("2. Log Experiment from file")
    print()
    print("3. Back to Experiment Menu")
    print("4. Back to Main Menu")
    print()

def exp_logging_menu_flow(db_path):
    """
    Experiment Logging menu flow.
    The parent flow is exp_menu_flow().
    This function will display the Experiment Logging menu and handle user input.
    Returns the result of the Experiment Logging menu.
    """
    while True:
        show_menu_title("Experiment Logging Menu")

        exp_logging_menu()
        choice = ask_a_menu_choice(["1", "2", "3", "4"])

        if choice == "1":
            result = log_experiment_flow_manually(db_path) # TODO: Refactor this function to return a result
        elif choice == "2":
            result = log_experiment_flow_from_file(db_path) # TODO: Implement this function
        elif choice == "3":
            result="exp menu"
            print("Returning to Experiment Menu...")
        elif choice == "4":
            result="main menu"
            print("Returning to Main Menu...")

        # Handle the result of the exp logging menu
        if result == "exp logging menu":
            continue
        elif result == "exp menu":
            return result
        elif result == "main menu":
            return result