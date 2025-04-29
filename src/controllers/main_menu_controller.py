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






def ask_menu_choice():
    return input("Enter your choice: ").strip()
                
def ask_a_choice(question:str, choices:list):
    """
    Ask the user a question and return their choice.
    """
    print(question)
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")
    
    while True:
        try:
            user_choice = int(input("Enter your choice: "))
            if 1 <= user_choice <= len(choices):
                return choices[user_choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def ask_yes_no(question:str):
    """
    Ask the user a yes/no question and return their answer.
    """
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def ask_for_string(question:str):
    """
    Ask the user for a string input.
    """
    while True:
        answer = input(f"{question}: ").strip()
        if answer:
            return answer
        else:
            print("Invalid input. Please enter a non-empty string.")

def ask_for_number(question:str):
    """
    Ask the user for a number input.
    """
    while True:
        try:
            answer = int(input(f"{question}: ").strip())
            return answer
        except ValueError:
            print("Invalid input. Please enter a number.")




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
        choice = ask_menu_choice()

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