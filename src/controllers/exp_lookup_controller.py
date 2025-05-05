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
        SELECT e.exp_date, s.name, t.name, a.name, st.name,
               m1.first_name || ' ' || m1.last_name,
               m2.first_name || ' ' || m2.last_name,
               m3.first_name || ' ' || m3.last_name
        FROM exp_log e
        JOIN species s ON e.species_id = s.id
        JOIN assay_type t ON e.assay_type_id = t.id
        JOIN assay a ON e.assay_id = a.id
        JOIN sample_type st ON e.sample_type_id = st.id
        LEFT JOIN manipulator m1 ON e.manipulator_1_id = m1.id
        LEFT JOIN manipulator m2 ON e.manipulator_2_id = m2.id
        LEFT JOIN manipulator m3 ON e.manipulator_3_id = m3.id
    """
    
    conditions = []
    params = []

    if date_filter:
        conditions.append("e.exp_date LIKE ?")
        params.append(f"{date_filter}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY e.exp_date DESC, a.name ASC"  # Newest dates first, alphabetical assay names

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