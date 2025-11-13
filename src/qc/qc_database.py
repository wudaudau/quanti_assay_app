

# File: src/qc/qc_database.py

import sqlite3

from src.database.db_utils import check_exists, get_or_insert

def insert_qc(
    db_path,
    qc_type,
    qc_name,
    qc_lot_number,
    manufacture_name=None,
    qc_cat_number=None,
    unit=None,
    expiration_date=None,
    preparation_date=None,
):
    """
    Insert a QC (purchased or homemade) and its analytes into the database.

    Parameters:
        db_path (str): Path to the database.
        qc_type (str): 'Purchased' or 'Home made'
        qc_name (str)
        qc_lot_number (str)
        manufacture_name (str | None)
        qc_cat_number (str | None)
        unit (str | None)
        expiration_date (str | None)
        preparation_date (str | None)
        analytes (list of (str, float)): List of (analyte_name, concentration)

    Returns:
        qc_id (int): ID of the inserted QC
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if QC lot number already exists in qc table
    if check_exists(cursor, "qc", {"lot_number": qc_lot_number}):
        print(f"QC with lot number '{qc_lot_number}' already exists.")
        return None

    # Get or insert manufacture
    manufacture_id = get_or_insert(cursor, "manufacturer", {"name": manufacture_name}) if manufacture_name else None

    # Insert into qc table
    cursor.execute("""
        INSERT INTO qc (
            qc_type, name, lot_number, manufacturer_id,
            cat_number, expiration_date, preparation_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        qc_type, qc_name, qc_lot_number, manufacture_id,
        qc_cat_number, expiration_date, preparation_date
    ))

    qc_id = cursor.lastrowid


    conn.commit()
    conn.close()

    return qc_id

def insert_qc_analyte(db_path, qc_id, analyte_name, concentration, unit):
    """
    Insert a QC analyte into the database.
    Parameters:
        db_path (str): Path to the database.
        qc_id (int): ID of the QC.
        analyte_name (str): Name of the analyte.
        concentration (float): Concentration of the analyte.
        unit (str): Unit of measurement.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get or insert analyte
    analyte_id = get_or_insert(cursor, "analyte", {"name": analyte_name})

    # Check existence
    if check_exists(cursor, "qc_analyte", {"qc_id": qc_id, "analyte_id": analyte_id}):
        raise ValueError(f"QC analyte '{analyte_name}' already exists for QC ID {qc_id}.") # TODO: Handle this case better


    # Insert into qc_analyte
    cursor.execute("""
        INSERT INTO qc_analyte (qc_id, analyte_id, concentration, unit)
        VALUES (?, ?, ?, ?)
    """, (qc_id, analyte_id, concentration, unit))

    conn.commit()
    conn.close()