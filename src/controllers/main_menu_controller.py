"""
"""


# Call controllers
from src.controllers.assay_lookup_controller import assay_lookup_flow

from src.controllers.assay_logging_controller import log_experiment_flow, lookup_experiments_flow

from src.controllers.qc_controller import (add_qc_flow, lookup_qc_flow)



def show_welcome():
    print("Welcome to QuantiApp - Assay Management System!")

def show_goodbye():
    print("Goodbye!")


def ask_user_choice():
    return input("Enter your choice: ").strip()
                





def show_main_menu():

    show_welcome()

    print("\nWaht do you want to do?")
    print("1. Assay Lookup")
    
    print("2. Log Experiment")
    print("3. Lookup Last 15 Experiments")
    print("4. Lookup All Experiments")
    print()
    print("7. Exit")

    print("8. Add a QC")
    print("9. Lookup a QC")

def main_menu_flow(db_path):
    """
    Main menu loop.
    """

    while True:
        show_main_menu()
        choice = ask_user_choice()

        if choice == "1":
            assay_lookup_flow(db_path)
        
            
        elif choice == "2":
            log_experiment_flow(db_path)
        elif choice == "3":
            lookup_experiments_flow(db_path, 15) # Limit to last 15 experiments
        elif choice == "4":
            lookup_experiments_flow(db_path)

        elif choice == "7":
            show_goodbye()
            break
        

        elif choice == "8":
            add_qc_flow(db_path)
        elif choice == "9":
            lookup_qc_flow(db_path)

            
        else:
            print("Invalid choice. Please try again.")