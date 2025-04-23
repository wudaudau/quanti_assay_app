"""
This file manages the main loop and application flow.

"""


# create db and import data
import os
from src_reform_app.src.database.db_core import create_database
from src_reform_app.src.database.db_data_loader import load_all_data_from_csv


# Call the controllers
from src_reform_app.src.controllers.assay_lookup_controller import (
    lookup_assay_details_full,
    lookup_assay_details_step_by_step,
    lookup_assay_details_by_species_and_analyte
)
from src_reform_app.src.controllers.assay_logging_controller import log_experiment_flow, lookup_experiments_flow



def show_welcome():
    print("Welcome to QuantiApp - Assay Management System!")

def show_goodbye():
    print("Goodbye!")


def show_main_menu():
    print("\nWaht do you want to do?")
    print("1. Lookup Assay (Full List)")
    print("2. Lookup Assay (Step-by-Step Filter)")
    print("3. Lookup Assay (Filter by Species and Analyte)")
    print("4. Log Experiment")
    print("5. Lookup Last 15 Experiments")
    print("6. Lookup All Experiments")
    print("7. Exit")

def ask_user_choice():
    return input("Enter your choice: ").strip()
                




def run_app():
    db_path = os.path.join("src_reform_app", "data", "reform_quantiapp.sqlite") # "../data/reform_quantiapp.sqlite"
    create_database(db_path)
    load_all_data_from_csv(db_path)



    show_welcome()
    while True:
        show_main_menu()
        choice = ask_user_choice()

        if choice == "1":
            lookup_assay_details_full(db_path)
        elif choice == "2":
            lookup_assay_details_step_by_step(db_path)
        elif choice == "3":
            lookup_assay_details_by_species_and_analyte(db_path)
        elif choice == "4":
            log_experiment_flow(db_path)
        elif choice == "5":
            lookup_experiments_flow(db_path, 15) # Limit to last 15 experiments
        elif choice == "6":
            lookup_experiments_flow(db_path)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")
    show_goodbye()

