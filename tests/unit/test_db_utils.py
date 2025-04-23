# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.database.db_utils import * # The code to test
import unittest # The test framework

import sqlite3

class TestDBUtils(unittest.TestCase):

    def setUp(self):
        # Use in-memory SQLite database for isolated testing
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        # Create a simple test table
        self.cursor.execute("""
            CREATE TABLE sample_type (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """)

    def tearDown(self):
        self.conn.close()

    def test_get_or_insert_inserts_new_value(self):
        sample_type = {"name": "Plasma"}
        new_id = get_or_insert(self.cursor, "sample_type", sample_type)
        self.conn.commit()

        self.cursor.execute("SELECT name FROM sample_type WHERE id = ?", (new_id,))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], "Plasma")

    def test_get_or_insert_retrieves_existing(self):
        # Insert manually
        self.cursor.execute("INSERT INTO sample_type (name) VALUES (?)", ("Serum",))
        self.conn.commit()

        existing_id = get_or_insert(self.cursor, "sample_type", {"name": "Serum"})
        self.conn.commit()

        # Confirm same value isn't duplicated
        self.cursor.execute("SELECT COUNT(*) FROM sample_type WHERE name = ?", ("Serum",))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_check_exists_returns_id(self):
        self.cursor.execute("INSERT INTO sample_type (name) VALUES (?)", ("CSF",))
        self.conn.commit()

        result = check_exists(self.cursor, "sample_type", {"name": "CSF"})
        self.assertIsNotNone(result)

    def test_check_exists_returns_none_for_missing(self):
        result = check_exists(self.cursor, "sample_type", {"name": "Urine"})
        self.assertIsNone(result)