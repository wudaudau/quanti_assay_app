
import sqlite3



######
# Lookup QC by Lot Nº
######

def fetch_last_10_qc_lot_from_db(db_path) -> list:
    """
    db_path: str. Path to the SQLite database.

    Fetch the last 10 QC lot numbers in alphabetic order from the database.
    Extract the QC lot numbers into a list.

    Return a list of QC lot numbers.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT lot_number FROM qc ORDER BY id DESC LIMIT 10;")
    qc_lots = cursor.fetchall()
    conn.close()

    ls_qc_lots = [qc_lot[0] for qc_lot in qc_lots]  # Extract names from tuples

    return ls_qc_lots

def get_qc_details_by_lot_part_1(db_path, qc_lot_number):
    """
    db_path: str. Path to the SQLite database.
    qc_lot_number: str. QC lot number to look up.

    Fetch QC details by lot number from the database.
    Return a list of tuples with QC details part 1.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT lot_number, qc_name, qc_type, manufacturer, cat_number, expiration_date, preparation_date
        FROM qc_lookup_view
        WHERE lot_number = ?;
    """, (qc_lot_number,))
    qc_details = cursor.fetchall() # TODO: Make sure only one row is returned
    conn.close()

    return qc_details # Return a list of tuples with QC details

def get_qc_details_by_lot_part_2(db_path, qc_lot_number):
    """
    db_path: str. Path to the SQLite database.
    qc_lot_number: str. QC lot number to look up.

    Fetch QC details by lot number from the database.
    Return a list of tuples with QC details part 2.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT analyte_name, concentration, unit
        FROM qc_lookup_view
        WHERE lot_number = ?;
    """, (qc_lot_number,))
    qc_details = cursor.fetchall() # TODO: Make sure only one row is returned
    conn.close()

    return qc_details # Return a list of tuples with QC details