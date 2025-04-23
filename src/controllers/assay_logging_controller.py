"""
"""

from datetime import datetime
import sqlite3
from src_reform_app.src.assay_logging.assay_logging import select_sample_type, select_manipulator, log_experiment
from src_reform_app.src.assay_lookup.assay_lookup import select_species, select_assay_type_by_species, select_assay_by_species_and_type

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


def log_experiment_flow(db_path):
    """
    """

    print("\n--- Starting Experiment Logging Process ---")
    print("Please follow the prompts to log your experiment.\n")

    # Placeholder for the upcoming steps (species selection, assay selection, etc.)
    # For now, just a simple message to confirm.
    print("This is where the experiment logging process will continue...")


    # Select species
    species = select_species(db_path)
    if not species:
        return

    species_id, species_name = species


    # Select assay type
    assay_type = select_assay_type_by_species(db_path, species_id)
    if not assay_type:
        return

    assay_type_id, assay_type_name = assay_type


    # Select assay
    assay = select_assay_by_species_and_type(db_path, species_id, assay_type_id)
    if not assay:
        return

    assay_id, assay_name = assay


    # Select sample type
    sample_type = select_sample_type(db_path)
    if not sample_type:
        return

    sample_type_id, sample_type_name = sample_type

    # Select manipulators
    manipulator_ids = ask_manipulator(db_path)


    exp_date = ask_experiment_date()
        
            

    log_experiment(db_path, species_id, assay_type_id, assay_id, sample_type_id, manipulator_ids, exp_date)

def lookup_experiments_flow(db_path, limit=None):
    """
    Lookup experiments log with optional date filter and optional limit (e.g., show last 15 logs).

    Args:
        db_path (str): Path to the database.
        limit (int, optional): Maximum number of logs to show, ordered by exp_date (newest first). Default is None (show all).
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    date_filter = input("Filter by date (YYYY-MM-DD or leave blank): ").strip()

    query = """
        SELECT e.exp_date, s.name, t.name, a.name, st.name,
               m1.first_name || ' ' || m1.last_name,
               m2.first_name || ' ' || m2.last_name,
               m3.first_name || ' ' || m3.last_name
        FROM exp_log e
        JOIN species s ON e.species_id = s.id
        JOIN assay_type t ON e.assay_type_id = t.id
        JOIN assay a ON e.assay_id = a.id
        JOIN sample_type st ON e.sample_type_id = st.id
        LEFT JOIN manipulator m1 ON e.manipulator_1_id = m1.id
        LEFT JOIN manipulator m2 ON e.manipulator_2_id = m2.id
        LEFT JOIN manipulator m3 ON e.manipulator_3_id = m3.id
    """
    
    conditions = []
    params = []

    if date_filter:
        conditions.append("e.exp_date LIKE ?")
        params.append(f"{date_filter}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY e.exp_date DESC, a.name ASC"  # Newest dates first, alphabetical assay names

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, tuple(params))

    rows = cursor.fetchall()
    conn.close()

    print("\nExperiments Log:")
    if not rows:
        print("No matching experiments found.")
        return

    for row in rows:
        print(row)