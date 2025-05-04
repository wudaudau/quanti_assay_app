"""
This is the Experiment menu controller module.
There are exp_menu and exp_menu_flow functions to display the Experiment menu and handle user input.
"""

from src.controllers.controller_utils import show_menu_title

from src.controllers.assay_logging_controller import log_experiment_flow, lookup_experiments_flow



def exp_menu():
    """
    Display the QC menu.
    """
    print("\nWhat do you want to do?")
    print("1. Log Experiment")
    print()
    print("2. Lookup Last 15 Experiments") # TODO: Make this a "Lookup menu"
    print("3. Lookup All Experiments")
    
    print()
    print("4. Back to Main Menu")

def exp_menu_flow(db_path):
    """
    Main menu loop.
    """
    while True:
        show_menu_title("Experiment Menu")
        exp_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            log_experiment_flow(db_path)
        elif choice == "2":
            lookup_experiments_flow(db_path, 15) # Limit to last 15 experiments
        elif choice == "3":
            lookup_experiments_flow(db_path)

        elif choice == "4":
            print("Returning to Main Menu...")
            break