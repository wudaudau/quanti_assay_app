"""
"""


# Call controllers

from src.controllers.controller_utils import show_goodbye # TODO: Move this to app.py?
from src.controllers.controller_utils import show_menu_title, ask_a_menu_choice


from src.controllers.assay_menu_controller import assay_menu_flow
from src.controllers.qc_menu_controller import qc_menu_flow
from src.controllers.exp_menu_controller import exp_menu_flow








def show_main_menu():

    print("\nWaht do you want to do?")

    print("1. Assay Menu")
    print("2. QC Menu")
    print("3. Experiment Menu")
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
        choice = ask_a_menu_choice(["1", "2", "3", "q"])

        if choice == "1":
            result = assay_menu_flow(db_path)
        elif choice == "2":
            result = qc_menu_flow(db_path)
        elif choice == "3":
            result = exp_menu_flow(db_path) # TODO: Update exp_menu_flow to return "main menu"
    
        elif choice == "q":
            show_goodbye()
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        


        # Handle the result of the assay lookup
        if result == "main menu":
            continue # restart the loop