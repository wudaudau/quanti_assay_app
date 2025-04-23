"""
Reusable helper functions like check_exists and get_or_insert, querying, checking, and inserting data into the database. 
"""

def check_exists(cursor, table, conditions):
    """
    Check if a row exists based on provided conditions.
    conditions: dict {column: value}
    """
    where_clause = " AND ".join([f"{col} = ?" for col in conditions])
    values = tuple(conditions.values())

    query = f"SELECT id FROM {table} WHERE {where_clause}"
    cursor.execute(query, values)
    return cursor.fetchone()

def get_or_insert(cursor, table, data):
    """
    Generic get_or_insert for tables with one or more unique columns.
    table: str
    data: dict {column: value}
    """
    row = check_exists(cursor, table, data)
    if row:
        return row[0]

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(insert_query, tuple(data.values()))
    return cursor.lastrowid

