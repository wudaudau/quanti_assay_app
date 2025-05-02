"""
This is the assay menu controller module.

There are assay_menu and assay_menu_flow functions to display the assay menu and handle user input.
"""


from src.controllers.messages_and_ask_questions import show_menu_title

from src.controllers.assay_lookup_controller import (
    assay_lookup_flow_details_full,
    assay_lookup_flow_details_step_by_step,
    assay_lookup_flow_details_by_species_and_analyte
)


def assay_menu():
    """
    Display the assay lookup menu.
    """
    print("\nWhat do you want to do?")
    # TODO: Add "new assay" option
    print("1. Lookup Assay (Full List)")
    print("2. Lookup Assay (Step-by-Step Filter)")
    print("3. Lookup Assay (Filter by Species and Analyte)")
    print()
    print("4. Back to Main Menu")

def assay_menu_flow(db_path):
    """
    Main menu loop.
    """
    while True:
        show_menu_title("Assay Lookup Menu")
        assay_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            result = assay_lookup_flow_details_full(db_path)
            if result is "assay menu":
                continue
            elif result is "main menu":
                return result # back to main_menu_flow()
        elif choice == "2":
            assay_lookup_flow_details_step_by_step(db_path)
        elif choice == "3":
            assay_lookup_flow_details_by_species_and_analyte(db_path)
        elif choice == "4":
            print("Returning to Main Menu...")
            break

