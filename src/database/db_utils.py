"""
Reusable helper functions like check_exists and get_or_insert, querying, checking, and inserting data into the database. 
"""

def check_exists(cursor, table:str, conditions:dict):
    """
    cursor: sqlite3.Cursor
    table: str. Table name to check.
    conditions: dict {column: value}

    Check if a row exists based on provided conditions.
    Returns the row ID if it exists, otherwise None.
    """
    where_clause = " AND ".join([f"{col} = ?" for col in conditions])
    values = tuple(conditions.values())

    query = f"SELECT id FROM {table} WHERE {where_clause}"
    cursor.execute(query, values)
    return cursor.fetchone()

def get_or_insert(cursor, table:str, data:dict):
    """
    cursor: sqlite3.Cursor
    table: str. Table name to check.
    data: dict {column: value}

    Generic get_or_insert for tables with one or more INIQUE columns.
    Checks if a row exists based on provided data.
    If it exists, returns the row ID. 
    If not, inserts the data and returns the new row ID.
    """
    row = check_exists(cursor, table, data)
    if row:
        return row[0]

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(insert_query, tuple(data.values()))
    return cursor.lastrowid

def update_row(cursor, table:str, id:int, data:dict):
    """
    cursor: sqlite3.Cursor
    table: str. Table name to update.
    id: int. Row ID to update.
    data: dict {column: value}

    Update a row in the specified table with the provided data.
    Returns the row id of the updated row.
    """
    set_clause = ", ".join([f"{col} = ?" for col in data])
    values = tuple(data.values()) + (id,)
    update_query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
    cursor.execute(update_query, values)
    return cursor.lastrowid # TODO: check if the row was updated and check if the row id is the same