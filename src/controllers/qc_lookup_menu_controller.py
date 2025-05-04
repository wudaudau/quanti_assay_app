"""
"""

from src.controllers.controller_utils import show_menu_title, ask_a_menu_choice, ask_a_menu_choice

from src.controllers.qc_lookup_controller import lookup_qc_flow_by_lot, lookup_qc_flow_by_assay, lookup_qc_flow_by_analyte

def qc_lookup_menu():
    """
    Display the QC lookup menu.
    """
    print("\nWhat do you want to do?")
    print("1. Lookup a QC by Lot Nº")
    print("2. Lookup a QC by Assay")
    print("3. Lookup a QC by Analyte")
    print()
    print("4. Back to QC Menu")
    print("5. Back to Main Menu")

def qc_lookup_menu_flow(db_path):
    """
    Main menu loop for QC lookup.
    """
    while True:
        show_menu_title("QC Lookup Menu")

        qc_lookup_menu()
        choice = ask_a_menu_choice(["1", "2", "3", "4", "5"])

        if choice == "1":
            result = lookup_qc_flow_by_lot(db_path) # TODO: Create this function
        elif choice == "2":
            result = lookup_qc_flow_by_assay(db_path)
        elif choice == "3":
            result = lookup_qc_flow_by_analyte(db_path)
        elif choice == "4":
            result = "qc menu"
            print("Returning to QC Menu...")
        elif choice == "5":
            result = "main menu"
            print("Returning to Main Menu...")


        # Handle the result of the assay lookup
        if result == "qc lookup menu":
            continue # restart the loop
        elif result == "qc menu":
            return result
        elif result == "main menu":
            return result