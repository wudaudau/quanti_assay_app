# Test the experiment logging database functions
import unittest
import sqlite3
import os
import tempfile
from src.database.exp_logging_db import (
    insert_experiment_raw, insert_well_data, insert_sd_preparation,
    insert_qc_concentrations, log_experiment_from_form
)


class TestExpLoggingDB(unittest.TestCase):

    def setUp(self):
        # Create temporary database for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create test tables (simplified versions)
        self.cursor.execute("""
            CREATE TABLE experiment_raw (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exp_date TEXT NOT NULL,
                species TEXT NOT NULL,
                assay_type TEXT NOT NULL,
                assay_name TEXT NOT NULL,
                sample_type TEXT NOT NULL,
                manipulator_1 TEXT NOT NULL,
                manipulator_2 TEXT,
                manipulator_3 TEXT,
                project_name TEXT,
                cohort_name TEXT,
                plate_layout_name TEXT,
                plate_bar_code TEXT,
                kit_cat_number TEXT NOT NULL,
                sd_cat_number TEXT,
                sd_lot_number TEXT,
                qc_h_lot_number TEXT,
                qc_m_lot_number TEXT,
                qc_l_lot_number TEXT,
                notes TEXT,
                UNIQUE(exp_date, assay_name, plate_layout_name)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE well_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_raw_id INTEGER NOT NULL,
                well_id TEXT NOT NULL,
                sample_name TEXT,
                sample_role TEXT,
                dilution_factor REAL,
                freeze_thaw_cycle INTEGER,
                excluded BOOLEAN DEFAULT 0,
                FOREIGN KEY (experiment_raw_id) REFERENCES experiment_raw(id),
                UNIQUE (experiment_raw_id, well_id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE sd_preparation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_raw_id INTEGER NOT NULL,
                sd7_concentration REAL,
                serial_dilution_factor REAL,
                sd7_unit TEXT,
                FOREIGN KEY (experiment_raw_id) REFERENCES experiment_raw(id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE qc_concentration (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_raw_id INTEGER NOT NULL,
                qc_l_concentration REAL,
                qc_m_concentration REAL,
                qc_h_concentration REAL,
                qc_unit TEXT,
                FOREIGN KEY (experiment_raw_id) REFERENCES experiment_raw(id)
            );
        """)

        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_insert_experiment_raw(self):
        """Test inserting experiment raw data"""
        exp_data = {
            'exp_date': '2025-01-15',
            'species': 'Human',
            'assay_type': 'ELISA',
            'assay_name': 'IL-6',
            'sample_type': 'Serum',
            'manipulator_1': 'John Doe',
            'kit_cat_number': 'KIT001',
            'plate_layout_name': 'Layout1'
        }

        exp_id = insert_experiment_raw(self.cursor, exp_data)
        self.conn.commit()

        # Verify insertion
        self.cursor.execute("SELECT * FROM experiment_raw WHERE id = ?", (exp_id,))
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], '2025-01-15')  # exp_date
        self.assertEqual(row[2], 'Human')       # species

    def test_insert_experiment_raw_missing_required_field(self):
        """Test that missing required fields raise ValueError"""
        exp_data = {
            'exp_date': '2025-01-15',
            'species': 'Human',
            # Missing assay_type
            'assay_name': 'IL-6',
            'sample_type': 'Serum',
            'manipulator_1': 'John Doe',
            'kit_cat_number': 'KIT001'
        }

        with self.assertRaises(ValueError) as context:
            insert_experiment_raw(self.cursor, exp_data)

        self.assertIn("Missing required field: assay_type", str(context.exception))

    def test_insert_well_data(self):
        """Test inserting well data"""
        # First insert an experiment
        exp_data = {
            'exp_date': '2025-01-15',
            'species': 'Human',
            'assay_type': 'ELISA',
            'assay_name': 'IL-6',
            'sample_type': 'Serum',
            'manipulator_1': 'John Doe',
            'kit_cat_number': 'KIT001',
            'plate_layout_name': 'Layout1'
        }
        exp_id = insert_experiment_raw(self.cursor, exp_data)

        # Insert well data
        well_data = [
            {'well_id': 'A01', 'sample_name': 'Sample1', 'sample_role': 'unknown'},
            {'well_id': 'A02', 'sample_name': 'Sample2', 'sample_role': 'unknown'}
        ]

        well_ids = insert_well_data(self.cursor, exp_id, well_data)
        self.conn.commit()

        # Verify insertion
        self.assertEqual(len(well_ids), 2)
        self.cursor.execute("SELECT COUNT(*) FROM well_data WHERE experiment_raw_id = ?", (exp_id,))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 2)

    def test_insert_sd_preparation(self):
        """Test inserting SD preparation data"""
        # First insert an experiment
        exp_data = {
            'exp_date': '2025-01-15',
            'species': 'Human',
            'assay_type': 'ELISA',
            'assay_name': 'IL-6',
            'sample_type': 'Serum',
            'manipulator_1': 'John Doe',
            'kit_cat_number': 'KIT001',
            'plate_layout_name': 'Layout1'
        }
        exp_id = insert_experiment_raw(self.cursor, exp_data)

        # Insert SD data
        sd_data = {
            'sd7_concentration': 100.0,
            'serial_dilution_factor': 2.0,
            'sd7_unit': 'pg/mL'
        }

        sd_id = insert_sd_preparation(self.cursor, exp_id, sd_data)
        self.conn.commit()

        # Verify insertion
        self.assertIsNotNone(sd_id)
        self.cursor.execute("SELECT * FROM sd_preparation WHERE id = ?", (sd_id,))
        row = self.cursor.fetchone()
        self.assertEqual(row[2], 100.0)  # sd7_concentration

    def test_insert_qc_concentrations(self):
        """Test inserting QC concentration data"""
        # First insert an experiment
        exp_data = {
            'exp_date': '2025-01-15',
            'species': 'Human',
            'assay_type': 'ELISA',
            'assay_name': 'IL-6',
            'sample_type': 'Serum',
            'manipulator_1': 'John Doe',
            'kit_cat_number': 'KIT001',
            'plate_layout_name': 'Layout1'
        }
        exp_id = insert_experiment_raw(self.cursor, exp_data)

        # Insert QC data
        qc_data = {
            'qc_l_concentration': 10.0,
            'qc_m_concentration': 50.0,
            'qc_h_concentration': 100.0,
            'qc_unit': 'pg/mL'
        }

        qc_id = insert_qc_concentrations(self.cursor, exp_id, qc_data)
        self.conn.commit()

        # Verify insertion
        self.assertIsNotNone(qc_id)
        self.cursor.execute("SELECT * FROM qc_concentration WHERE id = ?", (qc_id,))
        row = self.cursor.fetchone()
        self.assertEqual(row[2], 10.0)   # qc_l_concentration
        self.assertEqual(row[3], 50.0)   # qc_m_concentration
        self.assertEqual(row[4], 100.0)  # qc_h_concentration

    def test_log_experiment_from_form_basic(self):
        """Test the main log_experiment_from_form function with basic data"""
        form_data = {
            'exp_date': '2025-01-15',
            'species': 'Human',
            'assay_type': 'ELISA',
            'assay_name': 'IL-6',
            'sample_type': 'Serum',
            'manipulator_1': 'John Doe',
            'kit_cat_number': 'KIT001',
            'plate_layout_name': 'Layout1'
        }

        exp_id = log_experiment_from_form(self.db_path, form_data)

        # Verify the experiment was inserted
        self.cursor.execute("SELECT * FROM experiment_raw WHERE id = ?", (exp_id,))
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], '2025-01-15')


if __name__ == '__main__':
    unittest.main()