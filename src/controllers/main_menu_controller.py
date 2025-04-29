"""
"""


# Call controllers

from src.controllers.messages_and_ask_questions import show_goodbye # TODO: Move this to app.py?
from src.controllers.messages_and_ask_questions import show_menu_title, ask_a_menu_choice


from src.controllers.assay_lookup_controller import assay_lookup_flow

from src.controllers.assay_logging_controller import log_experiment_flow, lookup_experiments_flow

from src.controllers.qc_controller import (add_qc_flow, lookup_qc_flow)







def show_main_menu():

    print("\nWaht do you want to do?")

    print("1. Assay Lookup") # TODO: Make this "Assay Menu"
    print()
    
    print("2. Add a QC") # TODO: Make this "QC Menu"
    print("3. Lookup a QC")
    print()
    
    print("4. Log Experiment") # TODO: Make this "Experiment Menu"
    print("5. Lookup Last 15 Experiments")
    print("6. Lookup All Experiments")
    print()

    print("q. Exit")
    print()

def main_menu_flow(db_path):
    """
    Main menu loop.
    """

    while True:
        show_menu_title("Main Menu")

        show_main_menu()
        choice = ask_a_menu_choice()

        while choice not in ["1", "2", "3", "4", "q", "8", "9"]:
            print("Invalid choice. Please try again.")
            choice = ask_a_menu_choice()

        if choice == "1":
            assay_lookup_flow(db_path)

        
        elif choice == "2":
            add_qc_flow(db_path)
        elif choice == "3":
            lookup_qc_flow(db_path)
        
            
        elif choice == "4":
            log_experiment_flow(db_path)
        elif choice == "5":
            lookup_experiments_flow(db_path, 15) # Limit to last 15 experiments
        elif choice == "6":
            lookup_experiments_flow(db_path)

        elif choice == "q":
            show_goodbye()
            break
        
