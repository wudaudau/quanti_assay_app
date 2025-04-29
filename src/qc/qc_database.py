

# File: src/qc/qc_database.py

import sqlite3

def insert_qc(
    db_path,
    qc_type,
    qc_name,
    qc_lot_number,
    manufacturer_name=None,
    qc_cat_number=None,
    unit=None,
    expiration_date=None,
    preparation_date=None,
    analytes=None  # List of tuples: [(analyte_name, concentration), ...]
):
    """
    Insert a QC (purchased or homemade) and its analytes into the database.

    Parameters:
        db_path (str): Path to the database.
        qc_type (str): 'Purchased' or 'Home made'
        qc_name (str)
        qc_lot_number (str)
        manufacturer_name (str | None)
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

    # Get or insert manufacturer
    if manufacturer_name:
        cursor.execute("SELECT id FROM manufacture WHERE name = ?", (manufacturer_name,))
        row = cursor.fetchone()
        if row:
            manufacturer_id = row[0]
        else:
            cursor.execute("INSERT INTO manufacture (name) VALUES (?)", (manufacturer_name,))
            manufacturer_id = cursor.lastrowid
    else:
        manufacturer_id = None

    # Insert into qc table
    cursor.execute("""
        INSERT INTO qc (
            qc_type, name, lot_number, manufacturer_id,
            cat_number, unit, expiration_date, preparation_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        qc_type, qc_name, qc_lot_number, manufacturer_id,
        qc_cat_number, unit, expiration_date, preparation_date
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
            INSERT INTO qc_analyte (qc_id, analyte_id, concentration)
            VALUES (?, ?, ?)
        """, (qc_id, analyte_id, concentration))

    conn.commit()
    conn.close()

    return qc_id