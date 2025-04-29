"""
There are functions to set up the welcome and goodbye messages, and to ask the user for input.
"""

import datetime


def show_welcome():
    print("Welcome to QuantiApp - Assay Management System!")

def show_goodbye():
    print("Goodbye!")






def ask_a_menu_choice():
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
