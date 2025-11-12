"""
This is the Experiment menu controller module.
There are exp_menu and exp_menu_flow functions to display the Experiment menu and handle user input.
"""

from src.controllers.controller_utils import show_menu_title, ask_a_menu_choice

from src.controllers.exp_logging_menu_controller import exp_logging_menu_flow
from src.controllers.exp_lookup_menu_controller import exp_lookup_menu_flow


def exp_menu():
    """
    Display the QC menu.
    """
    print("\nWhat do you want to do?")
    print("1. Experiment Logging Menu")
    print("2. Experiment Lookup Menu")
    print()
    print("3. Back to Main Menu")

def exp_menu_flow(db_path):
    """
    Experiment menu flow.
    The parent flow is main_menu_flow().
    This function will display the Experiment menu and handle user input.
    Returns the result of the Experiment menu.
    """
    while True:
        show_menu_title("Experiment Menu")

        exp_menu()
        choice = ask_a_menu_choice(["1", "2", "3"])

        if choice == "1":
            result = exp_logging_menu_flow(db_path)
        elif choice == "2":
            result = exp_lookup_menu_flow(db_path)
        elif choice == "3":
            result="main menu"
            print("Returning to Main Menu...")


        # Handle the result of the exp menu
        if result == "exp menu":
            continue
        elif result == "main menu":
            return result