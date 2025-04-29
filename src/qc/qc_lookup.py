
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

    results = cursor.fetchall() # qc_lot is unique, so this should return at most one row per analyte
            # However, it can return multiple rows if there are multiple analytes for the same QC lot number
            # No multiplex QC for now, so this should be fine
    conn.close()

    
    # qc_name, lot_number, cat_number, expiration_date, preparation_date, manufacture_name, analyte_name, concentration, unit
    return results  # Returns a list of tuples with QC details