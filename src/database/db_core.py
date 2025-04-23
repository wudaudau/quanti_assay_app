"""
Core database functionality for the Reform app.
"""

import sqlite3

def connect_db(db_path):
    return sqlite3.connect(db_path)

def create_database(db_path):
    """
    Create the initial SQLite database file if it doesn't exist.
    For now, this just opens the connection to make sure the file exists.
    Later, we'll add table creation here.
    """
    conn = connect_db(db_path)

    with open("src_reform_app/sql/schema.sql", "r") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()

    conn.close()
    print(f"Database initialized at {db_path}")


