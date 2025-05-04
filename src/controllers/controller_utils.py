"""
There are functions to set up the welcome and goodbye messages, and to ask the user for input.
"""

import datetime


def show_welcome():
    print("Welcome to QuantiApp - Assay Management System!")

def show_goodbye():
    print("Thank you for using QuantiApp!")
    print("Goodbye!")


def show_menu_title(msg:str):
    """
    msg: str. Message to show in the menu title.
    This function will print a title for the menu.
    """
    print("\n" + "=" * 60)
    print(f"{msg:^60}")
    print("=" * 60)

def show_flow_title_and_descriptions(title:str, description:str):
    """
    title: str. Text to show in the flow title.
    description: str. Text to show in the flow description.
    This function will print a title and the description for the flow.
    """
    print()
    print(f"{title:=^60}")
    print()
    print("Description:")
    print(description)
    print()


def ask_a_menu_choice(menu_options:list) -> str:

    while True:
        choice = input("Enter your choice: ").strip()    

        if choice in menu_options:
            return choice
        else:
            print("Invalid choice. Please try again.")
                        
def ask_a_choice(question:str, choices:list) -> str:
    """
    question: str. The question to ask the user.
    choices: list. A list of choices to present to the user.
    
    Ask the user a question and return their choice.
    Returns the selected choice from the list.
    """
    print(question)
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")
    
    while True:
        try:
            user_choice = int(input("\nEnter your choice: "))
            if 1 <= user_choice <= len(choices):
                return choices[user_choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def ask_yes_no(question:str) -> bool:
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

def ask_for_date(question:str) -> datetime.date:
    """
    Ask the user for a date input.
    """
    while True:
        answer = input(f"{question} (YYYY-MM-DD): ").strip()
        try:
            year, month, day = map(int, answer.split('-'))
            return datetime.date(year, month, day)
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
