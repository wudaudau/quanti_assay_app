"""
This is the assay menu controller module.

There are assay_menu and assay_menu_flow functions to display the assay menu and handle user input.
"""


from src.controllers.controller_utils import show_menu_title, ask_a_menu_choice

from src.controllers.assay_lookup_controller import (
    assay_lookup_flow_no_filter,
    assay_lookup_flow_filter_by_species_and_assay_type,
    assay_lookup_flow_filter_by_species_and_analyte
)


def assay_menu():
    """
    Display the assay lookup menu.
    """
    print("\nWhat do you want to do?")
    # TODO: Add "new assay" option
    print("1. Lookup Assay (No Filter)")
    print("2. Lookup Assay (Filter by Species and Assay Type)")
    print("3. Lookup Assay (Filter by Species and Analyte)")
    print()
    print("4. Back to Main Menu")

def assay_menu_flow(db_path) -> str:
    """
    Assay menu flow.
    The parent flow is main_menu_flow().

    This function will display the assay menu and handle user input.
    Returns the result of the assay lookup.
    """
    while True:
        show_menu_title("Assay Lookup Menu")

        assay_menu()
        choice = ask_a_menu_choice(["1", "2", "3", "4"])

        if choice == "1":
            result = assay_lookup_flow_no_filter(db_path)
        elif choice == "2":
            result = assay_lookup_flow_filter_by_species_and_assay_type(db_path)
        elif choice == "3":
            result = assay_lookup_flow_filter_by_species_and_analyte(db_path)
        elif choice == "4":
            result="main menu"
            print("Returning to Main Menu...")
        

        # Handle the result of the assay menu
        if result == "assay menu":
            continue # restart the loop
        elif result == "main menu":
            return result # back to main_menu_flow()