"""
This module provides functions to look up assay details in a SQLite database.
This module connects between the database and the user interface (assay_lookup_controller).
"""


import sqlite3

def get_assay_details_by_name(db_path, assay_name):
    """
    Fetch assay details including species, assay type, and linked kits.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.name, s.name AS species, t.name AS assay_type, m.name AS manufacture, k.cat_number, k.format
        FROM assay a
        JOIN species s ON a.species_id = s.id
        JOIN assay_type t ON a.assay_type_id = t.id
        LEFT JOIN assays_kits ak ON a.id = ak.assay_id
        LEFT JOIN kit k ON ak.kit_id = k.id
        LEFT JOIN manufacture m ON k.manufacture_id = m.id
        WHERE a.name = ?
    """, (assay_name,))

    results = cursor.fetchall()
    conn.close()

    return results # Returns a list of (assay_name, species, assay_type, manufacture, kit_cat_number, format)

def get_analytes_for_assay(db_path, assay_name):
    """
    Retrieve all analytes linked to the given assay name, with spot numbers. Ordered by spot number.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT analyte.name, assays_analytes.spot_number
        FROM assay
        JOIN assays_analytes ON assay.id = assays_analytes.assay_id
        JOIN analyte ON assays_analytes.analyte_id = analyte.id
        WHERE assay.name = ?
        ORDER BY assays_analytes.spot_number
    """, (assay_name,))

    analytes = cursor.fetchall()  # List of (analyte_name, spot_number)
    conn.close()

    return analytes






######
# Assay Lookup
######


def select_assay_name(db_path):
    """
    CLI function to list and let user select an assay name.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM assay ORDER BY name;")
    assays = cursor.fetchall()
    conn.close()

    if not assays:
        print("No assays found in the database.")
        return None

    print("\nAvailable Assays:")
    for i, (assay_name,) in enumerate(assays, 1):
        print(f"{i}. {assay_name}")

    while True:
        try:
            choice = int(input("\nSelect an assay by number: "))
            if 1 <= choice <= len(assays):
                return assays[choice - 1][0]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")







######
# Step-by-Step Assay Lookup
######
# This is a new feature that allows the user to filter assays by species and assay type.
# The user can then select an assay from the filtered list and view its details.
# This is a more guided approach to finding an assay compared to the full list lookup.

def select_species(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM species ORDER BY name;")
    species = cursor.fetchall()
    conn.close()

    if not species:
        print("No species found in the database.")
        return None

    print("\nAvailable Species:")
    for i, (species_id, species_name) in enumerate(species, 1):
        print(f"{i}. {species_name}")

    while True:
        try:
            choice = int(input("\nSelect a species by number: "))
            if 1 <= choice <= len(species):
                return species[choice - 1]  # (id, name)
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def select_assay_type_by_species(db_path, species_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT at.id, at.name
        FROM assay a
        JOIN assay_type at ON a.assay_type_id = at.id
        WHERE a.species_id = ?
        ORDER BY at.name
    """, (species_id,))

    assay_types = cursor.fetchall()
    conn.close()

    if not assay_types:
        print("No assay types found for this species.")
        return None

    print("\nAvailable Assay Types:")
    for i, (assay_type_id, assay_type_name) in enumerate(assay_types, 1):
        print(f"{i}. {assay_type_name}")

    while True:
        try:
            choice = int(input("\nSelect an assay type by number: "))
            if 1 <= choice <= len(assay_types):
                return assay_types[choice - 1]  # (id, name)
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def select_assay_by_species_and_type(db_path, species_id, assay_type_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM assay
        WHERE species_id = ? AND assay_type_id = ?
        ORDER BY name
    """, (species_id, assay_type_id))

    assays = cursor.fetchall()
    conn.close()

    if not assays:
        print("No assays found for this species and assay type.")
        return None

    print("\nAvailable Assays:")
    for i, (assay_id, assay_name) in enumerate(assays, 1):
        print(f"{i}. {assay_name}")

    while True:
        try:
            choice = int(input("\nSelect an assay by number: "))
            if 1 <= choice <= len(assays):
                return assays[choice - 1]  # (id, name)
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")









######
# Lookup Assay by Analyte (by Species -> Analyte)
######

# Use select_species() from step-by-step lookup

def select_analyte_for_species(db_path, species_id):
    """
    List analytes linked to assays of a given species.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT analyte.id, analyte.name
        FROM assay
        JOIN assays_analytes ON assay.id = assays_analytes.assay_id
        JOIN analyte ON assays_analytes.analyte_id = analyte.id
        WHERE assay.species_id = ?
        ORDER BY analyte.name;
    """, (species_id,))

    analytes = cursor.fetchall()
    conn.close()

    if not analytes:
        print("No analytes found for this species.")
        return None

    print("\nAvailable Analytes:")
    for i, (analyte_id, analyte_name) in enumerate(analytes, 1):
        print(f"{i}. {analyte_name}")

    while True:
        try:
            choice = int(input("\nSelect an analyte by number: "))
            if 1 <= choice <= len(analytes):
                return analytes[choice - 1]
        except ValueError:
            pass
        print("Invalid input. Please enter a number.")

def select_assay_for_species_and_analyte(db_path, species_id, analyte_id):
    """
    List assays linked to the given species and analyte.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT assay.id, assay.name
        FROM assay
        JOIN assays_analytes ON assay.id = assays_analytes.assay_id
        WHERE assay.species_id = ? AND assays_analytes.analyte_id = ?
        ORDER BY assay.name;
    """, (species_id, analyte_id))

    assays = cursor.fetchall()
    conn.close()

    if not assays:
        print("No assays found for this species and analyte.")
        return None

    print("\nAvailable Assays:")
    for i, (assay_id, assay_name) in enumerate(assays, 1):
        print(f"{i}. {assay_name}")

    while True:
        try:
            choice = int(input("\nSelect an assay by number: "))
            if 1 <= choice <= len(assays):
                return assays[choice - 1]
        except ValueError:
            pass
        print("Invalid input. Please enter a number.")

