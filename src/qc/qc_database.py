

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
        raise ValueError(f"QC lot number '{qc_lot_number}' already exists in the database.") # TODO: Handle this case better

    # Get or insert manufacture
    manufacture_id = get_or_insert(cursor, "manufacture", {"name": manufacture_name}) if manufacture_name else None

    # Insert into qc table
    cursor.execute("""
        INSERT INTO qc (
            qc_type, name, lot_number, manufacture_id,
            cat_number, expiration_date, preparation_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        qc_type, qc_name, qc_lot_number, manufacture_id,
        qc_cat_number, expiration_date, preparation_date
    ))

    qc_id = cursor.lastrowid

    # Insert each analyte into qc_analyte table
    for analyte_name, concentration in analytes or []:
        # Get or insert analyte
        cursor.execute("SELECT id FROM analyte WHERE name = ?", (analyte_name,))
        row = cursor.fetchone()
        if row:
            analyte_id = row[0]
        else:
            cursor.execute("INSERT INTO analyte (name) VALUES (?)", (analyte_name,))
            analyte_id = cursor.lastrowid

        # Insert into qc_analyte
        cursor.execute("""
            INSERT INTO qc_analyte (qc_id, analyte_id, concentration, unit)
            VALUES (?, ?, ?, ?)
        """, (qc_id, analyte_id, concentration, unit))

    conn.commit()
    conn.close()

    return qc_id