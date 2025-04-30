"""
This is the QC menu controller module.
There are qc_menu and qc_menu_flow functions to display the QC menu and handle user input.
"""

from src.controllers.messages_and_ask_questions import show_menu_title

from src.controllers.qc_controller import (
    add_qc_flow,
    lookup_qc_flow
)


def qc_menu():
    """
    Display the QC menu.
    """
    print("\nWhat do you want to do?")
    print("1. Add a QC")
    print("2. Lookup a QC")
    print()
    print("3. Back to Main Menu")


def qc_menu_flow(db_path):
    """
    Main menu loop.
    """
    while True:
        show_menu_title("QC Menu")
        qc_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_qc_flow(db_path)
        elif choice == "2":
            lookup_qc_flow(db_path)
        elif choice == "3":
            print("Returning to Main Menu...")
            break

