# Test the CLI interface for experiment logging from file
import unittest
import sqlite3
import tempfile
import os
from unittest.mock import patch, MagicMock

from src.controllers.exp_logging_controller import log_experiment_flow_from_file


class TestExpLoggingCLI(unittest.TestCase):

    def setUp(self):
        # Create temporary database for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create minimal test tables
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

        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    @patch('builtins.input')
    @patch('src.controllers.exp_logging_controller.ask_yes_no')
    @patch('src.controllers.exp_logging_controller.ask_a_choice')
    @patch('src.controllers.exp_logging_controller.log_experiment_from_excel')
    @patch('src.controllers.exp_logging_controller.show_flow_title_and_descriptions')
    @patch('os.path.exists')
    def test_log_experiment_flow_from_file_success(self, mock_exists, mock_show, mock_log_excel,
                                                   mock_ask_choice, mock_ask_yes_no, mock_input):
        """Test successful experiment logging from file"""
        # Mock user inputs - order: form_version, file_path
        mock_input.side_effect = ["", "data/test.xlsx"]  # empty version (auto-detect), file path
        mock_ask_choice.return_value = "ELISA"
        mock_ask_yes_no.side_effect = [True, False]  # confirm processing, don't log another
        mock_exists.return_value = True
        mock_log_excel.return_value = 123

        # Run the function
        result = log_experiment_flow_from_file(self.db_path)

        # Verify the flow completed
        self.assertEqual(result, "exp logging menu")

        # Verify the Excel logging function was called correctly
        mock_log_excel.assert_called_once_with(
            db_path=self.db_path,
            excel_path="data/test.xlsx",
            assay_type="ELISA",
            form_version=None
        )

    @patch('builtins.input')
    @patch('src.controllers.exp_logging_controller.ask_yes_no')
    @patch('src.controllers.exp_logging_controller.ask_a_choice')
    @patch('src.controllers.exp_logging_controller.show_flow_title_and_descriptions')
    @patch('os.path.exists')
    def test_log_experiment_flow_from_file_file_not_found(self, mock_exists, mock_show,
                                                         mock_ask_choice, mock_ask_yes_no, mock_input):
        """Test handling of non-existent file then valid file"""
        # Mock user inputs - two iterations: bad file then good file
        mock_input.side_effect = ["", "nonexistent.xlsx", "", "", "data/test.xlsx"]  # version1, file1, continue, version2, file2
        mock_ask_choice.return_value = "MSD"
        mock_ask_yes_no.side_effect = [True, False]  # confirm second attempt, don't log another
        mock_exists.side_effect = [False, True]  # first file doesn't exist, second does
        mock_show.return_value = None

        # We need to patch log_experiment_from_excel too, but it's not in this test
        with patch('src.controllers.exp_logging_controller.log_experiment_from_excel') as mock_log_excel:
            mock_log_excel.return_value = 123
            
            # Run the function
            result = log_experiment_flow_from_file(self.db_path)

            # Verify the flow completed
            self.assertEqual(result, "exp logging menu")

            # Verify the Excel logging function was called for the valid file
            mock_log_excel.assert_called_once_with(
                db_path=self.db_path,
                excel_path="data/test.xlsx",
                assay_type="MSD",
                form_version=None
            )

    @patch('builtins.input')
    @patch('src.controllers.exp_logging_controller.ask_yes_no')
    @patch('src.controllers.exp_logging_controller.ask_a_choice')
    @patch('src.controllers.exp_logging_controller.log_experiment_from_excel')
    @patch('src.controllers.exp_logging_controller.show_flow_title_and_descriptions')
    @patch('os.path.exists')
    def test_log_experiment_flow_from_file_with_version(self, mock_exists, mock_show, mock_log_excel,
                                                       mock_ask_choice, mock_ask_yes_no, mock_input):
        """Test experiment logging with specific form version"""
        # Mock user inputs
        mock_input.side_effect = ["v210310", "data/test.xlsx"]  # version, file path
        mock_ask_choice.return_value = "MSD"
        mock_ask_yes_no.side_effect = [True, False]  # confirm, don't log another
        mock_exists.return_value = True
        mock_log_excel.return_value = 456

        # Run the function
        result = log_experiment_flow_from_file(self.db_path)

        # Verify the Excel logging function was called with version
        mock_log_excel.assert_called_once_with(
            db_path=self.db_path,
            excel_path="data/test.xlsx",
            assay_type="MSD",
            form_version="v210310"
        )

    @patch('builtins.input')
    @patch('src.controllers.exp_logging_controller.ask_yes_no')
    @patch('src.controllers.exp_logging_controller.ask_a_choice')
    @patch('src.controllers.exp_logging_controller.log_experiment_from_excel')
    @patch('src.controllers.exp_logging_controller.show_flow_title_and_descriptions')
    @patch('os.path.exists')
    def test_log_experiment_flow_from_file_user_cancel(self, mock_exists, mock_show, mock_log_excel,
                                                      mock_ask_choice, mock_ask_yes_no, mock_input):
        """Test user cancelling the operation"""
        # Mock user inputs
        mock_input.side_effect = ["", "data/test.xlsx"]  # empty version, file path
        mock_ask_choice.return_value = "ELISA"
        mock_ask_yes_no.return_value = False  # Don't confirm processing
        mock_exists.return_value = True

        # Run the function
        result = log_experiment_flow_from_file(self.db_path)

        # Should return to menu without processing
        self.assertEqual(result, "exp logging menu")

        # Verify Excel logging was not called
        mock_log_excel.assert_not_called()


if __name__ == '__main__':
    unittest.main()