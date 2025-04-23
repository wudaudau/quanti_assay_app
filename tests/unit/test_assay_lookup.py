# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.assay_lookup.assay_lookup import * # The code to test
import unittest # The test framework


import sqlite3


class TestAssayLookup(unittest.TestCase):

    def setUp(self):
        # Use in-memory SQLite database for isolated testing
        self.conn = sqlite3.connect(":memory:")
        self.create_schema()
        self.seed_data()

    def tearDown(self):
        self.conn.close()

    def create_schema(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
            CREATE TABLE species (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE assay_type (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE assay (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                species_id INTEGER NOT NULL,
                assay_type_id INTEGER NOT NULL,
                FOREIGN KEY (species_id) REFERENCES species(id),
                FOREIGN KEY (assay_type_id) REFERENCES assay_type(id)
            );

            CREATE TABLE analyte (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE assays_analytes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assay_id INTEGER NOT NULL,
                analyte_id INTEGER NOT NULL,
                spot_number INTEGER NOT NULL,
                FOREIGN KEY (assay_id) REFERENCES assay(id),
                FOREIGN KEY (analyte_id) REFERENCES analyte(id),
                UNIQUE (assay_id, analyte_id, spot_number)
            );
        """)
        self.conn.commit()

    def seed_data(self):
        cursor = self.conn.cursor()

        # Add species, assay type
        cursor.execute("INSERT INTO species (name) VALUES ('Human')")
        cursor.execute("INSERT INTO assay_type (name) VALUES ('MSD')")

        # Add assay
        cursor.execute("INSERT INTO assay (name, species_id, assay_type_id) VALUES ('Cytokine Panel 1', 1, 1)")

        # Add analytes
        cursor.execute("INSERT INTO analyte (name) VALUES ('IL-6')")
        cursor.execute("INSERT INTO analyte (name) VALUES ('TNF-alpha')")

        # Link analytes to assay with spot numbers
        cursor.execute("INSERT INTO assays_analytes (assay_id, analyte_id, spot_number) VALUES (1, 1, 1)")
        cursor.execute("INSERT INTO assays_analytes (assay_id, analyte_id, spot_number) VALUES (1, 2, 2)")

        self.conn.commit()

    def test_get_analytes_for_assay(self):
        analytes = get_analytes_for_assay(self.db_path, 'Cytokine Panel 1')
        self.assertEqual(len(analytes), 2)
        self.assertEqual(analytes, [('IL-6', 1), ('TNF-alpha', 2)])

    def test_get_analytes_for_non_existing_assay(self):
        analytes = get_analytes_for_assay(self.db_path, 'Non Existing Assay')
        self.assertEqual(len(analytes), 0)
