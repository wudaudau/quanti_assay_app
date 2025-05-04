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
        SELECT assay_name, species, assay_type, manufacture, kit_cat_number, format 
        FROM assay_lookup_view
        WHERE assay_name = ?
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
# Lookup Assay (No Filter)
######


def fetch_ls_assays_from_db(db_path) -> list:
    """
    db_path: str. Path to the SQLite database.

    Fetch all assay names in alphabetic order from the database.
    Extract the assay names into a list.

    Return a list of assay names.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM assay ORDER BY name;")
    assays = cursor.fetchall()
    conn.close()

    ls_assays = [assay[0] for assay in assays]  # Extract names from tuples

    return ls_assays







######
# Lookup Assay (Filter by Species and Assay Type)
######

def fetch_ls_species_from_db(db_path) -> list:
    """
    db_path: str. Path to the SQLite database.

    Fetch all species names in alphabetic order from the database.
    Extract the species names into a list.

    Return a list of species names.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM species ORDER BY name;")
    species = cursor.fetchall()
    conn.close()

    ls_species = [spec[0] for spec in species]  # Extract names from tuples

    return ls_species

def fetch_ls_assay_types_from_db_based_on_species(db_path, species:str) -> list:
    """
    db_path: str. Path to the SQLite database.
    species: str. Species name.

    Fetch all assay types linked to the given species in alphabetic order from the database.
    Extract the assay type names into a list.

    Return a list of assay type names.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT assay_type.name
        FROM assay
        JOIN assay_type ON assay.assay_type_id = assay_type.id
        JOIN species ON assay.species_id = species.id
        WHERE species.name = ?
        ORDER BY assay_type.name;
    """, (species,))

    assay_types = cursor.fetchall()
    conn.close()

    ls_assay_types = [assay_type[0] for assay_type in assay_types]  # Extract names from tuples

    return ls_assay_types

def fetch_ls_assays_from_db_based_on_species_and_assay_type(db_path, species:str, assay_type:str) -> list:
    """
    db_path: str. Path to the SQLite database.
    species: str. Species name.
    assay_type: str. Assay type name.

    Fetch all assay names linked to the given species and assay type in alphabetic order from the database.
    Extract the assay names into a list.

    Return a list of assay names.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT assay.name
        FROM assay
        JOIN assay_type ON assay.assay_type_id = assay_type.id
        JOIN species ON assay.species_id = species.id
        WHERE species.name = ? AND assay_type.name = ?
        ORDER BY assay.name;
    """, (species, assay_type))

    assays = cursor.fetchall()
    conn.close()

    ls_assays = [assay[0] for assay in assays]  # Extract names from tuples

    return ls_assays









######
# Lookup Assay (Filter by Species and Analyte)
######

# Use fetch_ls_species_from_db() from "Filter by Species and Assay Type" lookup

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

