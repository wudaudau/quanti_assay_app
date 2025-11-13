"""
"""


import sqlite3
from datetime import datetime
from src.database.db_utils import get_or_insert


def select_sample_type(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM sample_type ORDER BY name;")
    sample_types = cursor.fetchall()
    conn.close()

    if not sample_types:
        print("No sample types found in the database.")
        return None

    print("\nSample Types:")
    for i, (sample_type_id, sample_type) in enumerate(sample_types, 1):
        print(f"{i}. {sample_type}")

    while True:
        try:
            choice = int(input("\nSelect a sample type by number: "))
            if 1 <= choice <= len(sample_types):
                return sample_types[choice - 1] # (id, name)
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def select_manipulator(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, first_name, last_name FROM manipulator ORDER BY last_name, first_name;")
    manipulators = cursor.fetchall()
    conn.close()

    if not manipulators:
        print("No manipulators found in the database.")
        return None

    print("\nManipulators:")
    for i, (manipulator_id, first_name, last_name) in enumerate(manipulators, 1):
        print(f"{i}. {first_name} {last_name}")

    while True:
        try:
            choice = int(input("\nSelect a manipulator by number: "))
            if 1 <= choice <= len(manipulators):
                return manipulators[choice - 1] # (id, first_name, last_name)
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")



def log_experiment(db_path, species_id, assay_type_id, assay_id, sample_type_id, manipulator_ids, exp_date:str): # TODO: Rename to insert_experiment()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO exp_log (
            exp_date, species_id, assay_type_id, assay_id, sample_type_id,
            manipulator_1_id, manipulator_2_id, manipulator_3_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (exp_date, species_id, assay_type_id, assay_id, sample_type_id,
          manipulator_ids[0], manipulator_ids[1], manipulator_ids[2]))

    conn.commit()
    conn.close()
    print("Experiment logged successfully.")


def log_experiment_manual(db_path, species_name, assay_type, assay_name, sample_type_name, 
                         manipulator_names, exp_date, kit_cat_number):
    """
    Log a manually entered experiment to the experiment_raw table.
    
    Args:
        db_path: Path to the database
        species_name: Name of the species
        assay_type: Type of assay (MSD/ELISA)
        assay_name: Name of the assay
        sample_type_name: Name of the sample type
        manipulator_names: List of manipulator names (can include None)
        exp_date: Experiment date in YYYY-MM-DD format
        kit_cat_number: Kit catalog number
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO experiment_raw (
                exp_date, species, assay_type, assay_name, sample_type,
                manipulator_1, manipulator_2, manipulator_3, kit_cat_number
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (exp_date, species_name, assay_type, assay_name, sample_type_name,
              manipulator_names[0], manipulator_names[1], manipulator_names[2], kit_cat_number))

        conn.commit()
        print("Experiment logged successfully.")
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

