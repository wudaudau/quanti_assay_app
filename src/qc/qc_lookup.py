
import sqlite3


def get_qc_details_by_lot(db_path, qc_lot_number:str):
    """
    Fetch QC details by lot number.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT qc.name, qc.lot_number, qc.cat_number, qc.expiration_date, qc.preparation_date,
               m.name AS manufacture_name, a.name AS analyte_name, qa.concentration, qa.unit
        FROM qc
        LEFT JOIN manufacture m ON qc.manufacture_id = m.id
        LEFT JOIN qc_analyte qa ON qc.id = qa.qc_id
        LEFT JOIN analyte a ON qa.analyte_id = a.id
        WHERE qc.lot_number = ?
    """, (qc_lot_number,))

    results = cursor.fetchall()
    conn.close()

    return results  # Returns a list of tuples with QC details