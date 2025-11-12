"""
Experiment logging controller - handles user interaction for logging experiments
"""

from datetime import datetime
import sqlite3

from src.controllers.controller_utils import show_flow_title_and_descriptions, ask_a_choice, ask_yes_no
from src.assay_logging.assay_logging import select_sample_type, select_manipulator, log_experiment
from src.assay_lookup.assay_lookup import (fetch_ls_species_from_db, fetch_ls_assay_types_from_db_based_on_species,
                                           fetch_ls_assays_from_db_based_on_species_and_assay_type
                                             )
from src.data_import.exp_reader import log_experiment_from_excel

def ask_manipulator(db_path):
    """
    CLI function to ask the user to select up to 3 manipulators.

    Returns a list of exactly 3 manipulator IDs (some can be None if skipped).
    """
    manipulator_ids = []

    for i in range(3):
        if i == 0:
            print("\nSelect first manipulator:")
        elif i == 1:
            print("\nSelect second manipulator:")
        elif i == 2:
            print("\nSelect third manipulator:")

        manipulator = select_manipulator(db_path)

        if manipulator:
            manipulator_ids.append(manipulator[0])
        else:
            manipulator_ids.append(None)

        if i < 2:  # Only ask to continue after first and second manipulator
            while True:
                cont = input("Do you want to add another manipulator? (y/n): ").strip().lower()
                
                if cont == "y":
                    break  # User wants to continue, so move to the next manipulator
                elif cont == "n":
                    # Fill the rest with None if they don't want to continue
                    while len(manipulator_ids) < 3:
                        manipulator_ids.append(None)
                    return manipulator_ids  # Early return to exit the loop
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")  # Prompt again if invalid

    

    return manipulator_ids

def ask_experiment_date():
    """
    CLI function to ask the user for the experiment date.

    Returns a string in ISO format. Example: "2021-07-15"
    """
    while True:
        exp_date = input("Enter the experiment date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(exp_date, '%Y-%m-%d')
            return exp_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def log_experiment_flow_manually(db_path):
    """

    (This function is similar to assay_lookup_flow_filter_by_species_and_assay_type() in assay_lookup_controller.py) # TODO: Refactor to avoid duplication using modules?

    Before logging the experiment, we need to have qc data
    """

    while True:
        show_flow_title_and_descriptions("Log an Experiment", 
                                         "Please follow the prompts to log your experiment.")


        # Placeholder for the upcoming steps (species selection, assay selection, etc.)
        # For now, just a simple message to confirm.
        print("This is where the experiment logging process will continue...")


        # 1) Ask species:
            # Obtain species list from the database
            # Use ask_a_choice() to show the list and get the user's choice
        ls_species = fetch_ls_species_from_db(db_path)
        if len(ls_species) == 0: # TODO: We need to test this case
            print("No species found in the database.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            species_name = ask_a_choice("\nAvailable Species:", ls_species)


        # 2) Ask assay type:
        ls_assay_type = fetch_ls_assay_types_from_db_based_on_species(db_path, species_name)
        if len(ls_assay_type) == 0: # TODO: We need to test this case
            print("No assay types found for this species.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            assay_type = ask_a_choice("\nAvailable Assay Types:", ls_assay_type)


        # 3) Ask assay name:
        ls_assays = fetch_ls_assays_from_db_based_on_species_and_assay_type(db_path, species_name, assay_type)
        if len(ls_assays) == 0: # TODO: We need to test this case
            print("No assays found for this species and assay type.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            assay_name = ask_a_choice("\nAvailable Assays:", ls_assays)


        # Select sample type
        sample_type = select_sample_type(db_path)
        if not sample_type:
            return

        sample_type_id, sample_type_name = sample_type

        # Select manipulators
        manipulator_ids = ask_manipulator(db_path)


        exp_date = ask_experiment_date()



        # Review the selected options
        # TODO: Add the review and confirmation step
            
                
        # TODO: Refactor this
        # log_experiment(db_path, species_id, assay_type_id, assay_id, sample_type_id, manipulator_ids, exp_date)
        print("(We need to refactor log_experiment() to log the data more efficiently.)")

def log_experiment_flow_from_file(db_path):
    """
    CLI flow for logging an experiment from an Excel file.
    Guides the user through selecting assay type/version and file path,
    then parses and logs the experiment to the database.
    """

    while True:
        show_flow_title_and_descriptions("Log an Experiment from File",
                                         "Please follow the prompts to log your experiment from a file.")

        # 1) Ask assay type
        print("\nSelect the assay type for your experiment:")
        print("1. MSD")
        print("2. ELISA")

        assay_type_choice = ask_a_choice("Assay Type:", ["MSD", "ELISA"])
        assay_type = assay_type_choice

        # 2) Ask form version (optional - can auto-detect)
        print(f"\nFor {assay_type}, you can specify a form version or let the system auto-detect it.")
        print("Common versions: v210305, v210310, v211019, v220907, v230306, v240104, v250227")
        print("(Press Enter to auto-detect)")

        form_version = input("Form version (optional): ").strip()
        if not form_version:
            form_version = None

        # 3) Ask for file path
        print("\nPlease enter the path to your Excel experiment file:")
        print("Example: data/experiment_file.xlsx")

        file_path = input("File path: ").strip()

        if not file_path:
            print("No file path provided. Returning to menu...")
            return "exp logging menu"

        # Check if file exists
        import os
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            print("Please check the file path and try again.")
            input("\nPress Enter to continue...")
            continue

        # 4) Confirm before processing
        print(f"\nReady to process:")
        print(f"  File: {file_path}")
        print(f"  Assay Type: {assay_type}")
        print(f"  Form Version: {form_version or 'Auto-detect'}")

        confirm = ask_yes_no("\nProceed with logging this experiment?")
        if not confirm:
            print("Operation cancelled. Returning to menu...")
            return "exp logging menu"

        # 5) Process the file
        try:
            print("\nProcessing Excel file...")
            exp_id = log_experiment_from_excel(
                db_path=db_path,
                excel_path=file_path,
                assay_type=assay_type,
                form_version=form_version
            )

            print("✅ Experiment logged successfully!")
            print(f"   Experiment ID: {exp_id}")
            print(f"   File processed: {file_path}")

            # Ask if user wants to log another experiment
            another = ask_yes_no("\nWould you like to log another experiment from file?")
            if another:
                continue
            else:
                return "exp logging menu"

        except ValueError as e:
            print(f"❌ Error processing file: {e}")
            print("Please check your file format and try again.")
            input("\nPress Enter to continue...")
            continue
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("Please contact support if this persists.")
            input("\nPress Enter to continue...")
            continue