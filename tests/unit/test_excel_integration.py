# Test the Excel parsing integration with database logging
import unittest
import sqlite3
import tempfile
import os
from unittest.mock import patch, MagicMock
import pandas as pd

from src.data_import.exp_reader import log_experiment_from_excel, transform_extracted_data_to_db_format


class TestExcelIntegration(unittest.TestCase):

    def setUp(self):
        # Create temporary database for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create test tables (simplified versions matching the schema)
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
            CREATE TABLE readout (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                well_data_id INTEGER NOT NULL,
                analyte_name TEXT NOT NULL,
                value REAL,
                readout_type TEXT DEFAULT 'raw',
                FOREIGN KEY (well_data_id) REFERENCES well_data(id)
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

    def test_transform_extracted_data_to_db_format(self):
        """Test transformation of extracted data to database format"""
        extracted_data = {
            "exp_log": {
                "exp_date": "2025-01-15",
                "species": "Human",
                "assay_type": "ELISA",
                "assay_name": "IL-6",
                "sample_type": "Serum",
                "manipulator_1": "John Doe",
                "manipulator_2": "Jane Smith",
                "project_name": "Project A",
                "cohort_name": "Cohort 1",
                "plate_layout_name": "Layout1",
                "kit_cat_number": "KIT001",
                "sd_cat_number": "SD001",
                "sd_lot_number": "LOT001",
                "qc_h_lot_number": "QC001",
                "notes": "Test experiment"
            },
            "sd_preparation": {
                "sd7_concentration": 100.0,
                "serial_dilution_factor": 2.0
            },
            "well_data": pd.DataFrame({
                "sample_name": ["Sample1", "Sample2"],
                "sample_role": ["unknown", "standard"]
            }, index=["A01", "A02"]),
            "readouts": pd.DataFrame({
                "IL-6": [10.5, 20.3],
                "TNF-alpha": [5.2, 8.1]
            }, index=["A01", "A02"])
        }

        db_data = transform_extracted_data_to_db_format(extracted_data)

        # Check main experiment data
        self.assertEqual(db_data["exp_date"], "2025-01-15")
        self.assertEqual(db_data["species"], "Human")
        self.assertEqual(db_data["assay_type"], "ELISA")
        self.assertEqual(db_data["assay_name"], "IL-6")
        self.assertEqual(db_data["manipulator_1"], "John Doe")
        self.assertEqual(db_data["manipulator_2"], "Jane Smith")

        # Check SD preparation
        self.assertIn("sd_preparation", db_data)
        self.assertEqual(db_data["sd_preparation"]["sd7_concentration"], 100.0)
        self.assertEqual(db_data["sd_preparation"]["serial_dilution_factor"], 2.0)

        # Check well data
        self.assertIn("well_data", db_data)
        self.assertEqual(len(db_data["well_data"]), 2)
        self.assertEqual(db_data["well_data"][0]["well_id"], "A01")
        self.assertEqual(db_data["well_data"][0]["sample_name"], "Sample1")

        # Check readout data
        self.assertIn("readout_data", db_data)
        self.assertIn("A01", db_data["readout_data"])
        self.assertEqual(len(db_data["readout_data"]["A01"]), 2)  # 2 analytes

    @patch('src.data_import.exp_reader.load_exp_form')
    @patch('src.data_import.exp_reader.extract_exp_data')
    def test_log_experiment_from_excel_integration(self, mock_extract, mock_load):
        """Test the full integration of Excel parsing to database logging"""
        # Mock the form loading
        mock_form = MagicMock()
        mock_load.return_value = mock_form

        # Mock the data extraction
        mock_extract.return_value = {
            "exp_log": {
                "exp_date": "2025-01-15",
                "species": "Human",
                "assay_type": "ELISA",
                "assay_name": "IL-6",
                "sample_type": "Serum",
                "manipulator_1": "John Doe",
                "plate_layout_name": "TestLayout",
                "kit_cat_number": "KIT001"
            },
            "sd_preparation": {},
            "well_data": pd.DataFrame({
                "sample_name": ["Sample1"],
                "sample_role": ["unknown"]
            }, index=["A01"]),
            "readouts": None
        }

        # Test the integration
        exp_id = log_experiment_from_excel(self.db_path, "dummy.xlsx", "ELISA", "v201222")

        # Verify the form loading was called correctly
        mock_load.assert_called_once_with("dummy.xlsx", "ELISA", "v201222")

        # Verify data was inserted
        self.cursor.execute("SELECT * FROM experiment_raw WHERE id = ?", (exp_id,))
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "2025-01-15")  # exp_date
        self.assertEqual(row[2], "Human")       # species

    def test_sd_lot_number_list_handling(self):
        """Test that SD lot number lists are handled correctly"""
        extracted_data = {
            "exp_log": {
                "exp_date": "2025-01-15",
                "species": "Human",
                "assay_type": "MSD",
                "assay_name": "Cytokine Panel",
                "sample_type": "Serum",
                "manipulator_1": "John Doe",
                "plate_layout_name": "TestLayout",
                "kit_cat_number": "KIT001",
                "sd_lot_number": ["LOT001", "LOT002", "LOT003"]  # List of lots
            }
        }

        db_data = transform_extracted_data_to_db_format(extracted_data)

        # Should take the first lot number from the list
        self.assertEqual(db_data["sd_lot_number"], "LOT001")

    def test_empty_sd_lot_number_list_handling(self):
        """Test that empty SD lot number lists are handled correctly"""
        extracted_data = {
            "exp_log": {
                "exp_date": "2025-01-15",
                "species": "Human",
                "assay_type": "MSD",
                "assay_name": "Cytokine Panel",
                "sample_type": "Serum",
                "manipulator_1": "John Doe",
                "plate_layout_name": "TestLayout",
                "kit_cat_number": "KIT001",
                "sd_lot_number": []  # Empty list
            }
        }

        db_data = transform_extracted_data_to_db_format(extracted_data)

        # Should be None for empty list
        self.assertIsNone(db_data["sd_lot_number"])


if __name__ == '__main__':
    unittest.main()