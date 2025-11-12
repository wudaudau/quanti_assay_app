"""
"""

import sqlite3



def lookup_experiments_flow(db_path, limit=None):
    """
    Lookup experiments log with optional date filter and optional limit (e.g., show last 15 logs).

    Args:
        db_path (str): Path to the database.
        limit (int, optional): Maximum number of logs to show, ordered by exp_date (newest first). Default is None (show all).
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    date_filter = input("Filter by date (YYYY-MM-DD or leave blank): ").strip()

    # TODO: Move this to a function in src.assay_logging.assay_logging?
    query = """
        SELECT e.exp_date, e.species, e.assay_type, e.assay_name, e.sample_type,
               e.manipulator_1, e.manipulator_2, e.manipulator_3
        FROM experiment_raw e
    """
    
    conditions = []
    params = []

    if date_filter:
        conditions.append("e.exp_date LIKE ?")
        params.append(f"{date_filter}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY e.exp_date DESC, e.assay_name ASC"  # Newest dates first, alphabetical assay names

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, tuple(params))

    rows = cursor.fetchall()
    conn.close()

    print("\nExperiments Log:")
    if not rows:
        print("No matching experiments found.")
        return

    for row in rows:
        print(row)