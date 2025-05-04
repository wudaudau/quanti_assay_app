"""
Functions responsible for reading CSV files and bulk-inserting data into tables.
CSV files are saved as 

There are following csv files to import:
- assays.csv: assay_name, assay_type, species -> 
- assays_kits.csv: assay_name, manufacturer, kit_cat_number ->
- assay_analytes.csv: assay_name, spot_number, analyte_name -> 
- sample_types.csv: name ->
- manipulators.csv: first_name, last_name ->
"""

import sqlite3
import csv
from src.database.db_utils import get_or_insert, update_row



def load_all_data_from_csv(db_path):
    """
    Central function to load all data from CSV files into the database.
    Keeps app.py clean.
    """
    print("\n--- Importing Initial Data from CSV Files ---")

    add_assays_from_csv(db_path, 'data/assays.csv')
    add_assays_kits_from_csv(db_path, 'data/assays_kits.csv')
    add_assays_analytes_from_csv(db_path, 'data/assays_analytes.csv')
    add_sample_types_from_csv(db_path, 'data/sample_types.csv')
    add_qc_from_csv(db_path, 'data/qc.csv')
    add_manipulators_from_csv(db_path, 'data/manipulators.csv')

    print("--- Data Import Complete ---\n")







def add_assays_from_csv(db_path, csv_file):
    """assays.csv: assay_name, assay_type, species"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            assay_name = row['assay_name']
            assay_type = row['assay_type']
            species = row['species']

            species_id = get_or_insert(cursor, 'species', {'name': species})
            assay_type_id = get_or_insert(cursor, 'assay_type', {'name': assay_type})

            # Insert into assay table (skip if exists due to UNIQUE constraint on name)
            cursor.execute("""
                INSERT OR IGNORE INTO assay (name, species_id, assay_type_id)
                VALUES (?, ?, ?)
            """, (assay_name, species_id, assay_type_id))

    conn.commit()
    conn.close()
    print(f"Assays from {csv_file} imported.")

def add_assays_kits_from_csv(db_path, csv_file):
    """
    assays_kits.csv: assay_name, manufacturer, kit_cat_number
    
    We need to:
    1. Obtain (or insert) the assay_id, manufacturer_id, and kit_id from the respective tables.
    2. Insert the mapping into the assays_kits table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Assay information
            assay_name = row['assay_name'] # Need to obtain the assay_id from the assay table

            # Kit information
            manufacturer = row['manufacturer'] # Need to obtain the manufacturer_id from the manufacturer table
            kit_cat_number = row['kit_cat_number']
            kit_format = row.get('format', None)  # Safe handling if 'format' is missing


            # Obtain ids (on unique columns)
            assay_id = get_or_insert(cursor, 'assay', {'name': assay_name})
            manufacturer_id = get_or_insert(cursor, 'manufacturer', {'name': manufacturer})
            kit_id = get_or_insert(cursor, 'kit', {'manufacturer_id': manufacturer_id, 'cat_number': kit_cat_number})

            # Update kit format if provided
            update_row(cursor, 'kit', kit_id, {'format': kit_format}) if kit_format else None

            # Insert into assays_kits table
            cursor.execute("""
                INSERT OR IGNORE INTO assays_kits (assay_id, kit_id)
                VALUES (?, ?)
            """, (assay_id, kit_id))

    conn.commit()
    conn.close()
    print(f"Kits from {csv_file} imported.")



def add_assays_analytes_from_csv(db_path, csv_file):
    """
    Read assay_analytes.csv and insert assay-analyte mappings into the database.
    Includes spot_number to handle multi-analyte panels.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            assay_name = row['assay_name']
            spot_number = int(row['spot_number'])
            analyte_name = row['analyte_name']

            # Lookup assay_id
            cursor.execute("SELECT id FROM assay WHERE name = ?", (assay_name,))
            assay_row = cursor.fetchone()

            if not assay_row:
                print(f"Warning: Assay '{assay_name}' not found when adding analyte '{analyte_name}'. Skipping.")
                continue

            assay_id = assay_row[0]

            # Get or insert analyte
            analyte_id = get_or_insert(cursor, 'analyte', {'name': analyte_name})

            # Insert into assays_analytes (skip if already exists)
            cursor.execute("""
                INSERT OR IGNORE INTO assays_analytes (assay_id, analyte_id, spot_number)
                VALUES (?, ?, ?)
            """, (assay_id, analyte_id, spot_number))

    conn.commit()
    conn.close()
    print(f"Assay-analyte links from {csv_file} imported.")

def add_sample_types_from_csv(db_path, csv_file):
    """Read sample_types.csv and insert sample types into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            sample_type = row['name']

            # Insert into sample_type table (skip if exists due to UNIQUE constraint on name)
            cursor.execute("""
                INSERT OR IGNORE INTO sample_type (name)
                VALUES (?)
            """, (sample_type,))

    conn.commit()
    conn.close()
    print(f"Sample types from {csv_file} imported.")

def add_qc_from_csv(db_path, csv_file):
    """
    qc.csv: lot_number, qc_name, analyte, concentration, unit, qc_type, manufacturer, cat_number, expiration_date, preparation_date, note

    We need to:
    1. Obtain (or insert) the analyte_id, and sample_type_id from the respective tables.
    2. Insert the mapping into the qc_analytes table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            lot_number = row['lot_number']
            qc_name = row['qc_name']
            analyte = row['analyte']
            concentration = row['concentration']
            unit = row['unit']
            qc_type = row['qc_type'] # "Purchased" or "Home made"
            manufacturer = row['manufacturer'] # TODO: Use row.get()?
            cat_number = row['cat_number'] # TODO: Use row.get()?
            expiration_date = row['expiration_date']
            preparation_date = row['preparation_date']
            note = row['note']

            # Obtain ids (on unique columns)
            analyte_id = get_or_insert(cursor, 'analyte', {'name': analyte})
            manufacturer_id = get_or_insert(cursor, 'manufacturer', {'name': manufacturer})


            qc_id = get_or_insert(cursor, 'qc', {'lot_number': lot_number, 'name': qc_name, 'qc_type': qc_type})
            # TODO: We may need to check if the lot_number already exists in the qc table to handle duplicates from the CSV file

            # Updeate qc table with additional information
            update_row(cursor, 'qc', qc_id, {
                'manufacturer_id': manufacturer_id,
                'cat_number': cat_number,
                'expiration_date': expiration_date,
                'preparation_date': preparation_date,
                'note': note 
            })


            # Insert into qc table (skip if exists due to UNIQUE constraint on lot_number)
            cursor.execute("""
                INSERT OR IGNORE INTO qc_analyte (qc_id, analyte_id, concentration, unit)
                VALUES (?, ?, ?, ?)
            """, (qc_id, analyte_id, concentration, unit))
                
    conn.commit()
    conn.close()
    print(f"QC data from {csv_file} imported.")


def add_manipulators_from_csv(db_path, csv_file):
    """Read manipulators.csv and insert manipulators into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']

            # Insert into manipulator table (skip if exists due to UNIQUE constraint on email)
            cursor.execute("""
                INSERT OR IGNORE INTO manipulator (first_name, last_name)
                VALUES (?, ?)
            """, (first_name, last_name))

    conn.commit()
    conn.close()
    print(f"Manipulators from {csv_file} imported.")