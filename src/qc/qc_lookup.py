
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


######
# Lookup QC by Assay
######

def fetch_qc_assays_from_db(db_path) -> list:
    """
    db_path: str. Path to the SQLite database.

    Fetch all unique QC assay names from the database.

    Return a list of QC assay names.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT qc_name FROM qc_lookup_view ORDER BY qc_name;")
    qc_assays = cursor.fetchall()
    conn.close()

    ls_qc_assays = [qc_assay[0] for qc_assay in qc_assays]  # Extract names from tuples

    return ls_qc_assays


def get_qc_details_by_assay(db_path, qc_assay_name):
    """
    db_path: str. Path to the SQLite database.
    qc_assay_name: str. QC assay name to look up.

    Fetch QC details by assay name from the database.
    Return a list of tuples with QC details.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT qc_name, qc_type, manufacturer, cat_number, lot_number, preparation_date, expiration_date
        FROM qc_lookup_view
        WHERE qc_name = ?;
    """, (qc_assay_name,))
    qc_details = cursor.fetchall()
    conn.close()

    return qc_details


######
# Lookup QC by Analyte
######

def fetch_qc_analytes_from_db(db_path) -> list:
    """
    db_path: str. Path to the SQLite database.

    Fetch all unique QC analyte names from the database.

    Return a list of QC analyte names.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT analyte_name FROM qc_lookup_view ORDER BY analyte_name;")
    qc_analytes = cursor.fetchall()
    conn.close()

    ls_qc_analytes = [qc_analyte[0] for qc_analyte in qc_analytes]  # Extract names from tuples

    return ls_qc_analytes


def get_qc_details_by_analyte(db_path, qc_analyte_name):
    """
    db_path: str. Path to the SQLite database.
    qc_analyte_name: str. QC analyte name to look up.

    Fetch QC details by analyte name from the database.
    Return a list of tuples with QC details.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT qc_name, lot_number, concentration, unit, qc_type, manufacturer, cat_number, preparation_date, expiration_date
        FROM qc_lookup_view
        WHERE analyte_name = ?;
    """, (qc_analyte_name,))
    qc_details = cursor.fetchall()
    conn.close()

    return qc_details