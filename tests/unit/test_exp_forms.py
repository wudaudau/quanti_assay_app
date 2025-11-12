# Test the refactored exp_forms structure
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

# Test imports work
try:
    from src.data_import.exp_forms.base import ReadExpInfo
    from src.data_import.exp_forms.msd_versions.v210305 import ExpFormMsdV210305
    from src.data_import.exp_forms.elisa_versions.v201222 import ExpFormElisaV201222
    from src.data_import.exp_reader import load_exp_form
    IMPORTS_WORK = True
    IMPORT_ERROR = None
except ImportError as e:
    IMPORTS_WORK = False
    IMPORT_ERROR = str(e)


class TestExpFormsRefactoring(unittest.TestCase):

    def test_imports_work(self):
        """Test that all refactored imports work correctly"""
        self.assertTrue(IMPORTS_WORK, f"Imports failed: {IMPORT_ERROR}")

    @patch('src.data_import.exp_forms.base.openpyxl.load_workbook')
    def test_base_class_instantiation(self, mock_load_workbook):
        """Test that the base ReadExpInfo class can be instantiated"""
        # Mock the workbook
        mock_wb = MagicMock()
        mock_ws = MagicMock()
        mock_wb.__getitem__.return_value = mock_ws
        mock_load_workbook.return_value = mock_wb

        # Mock worksheet data
        mock_ws.cell.side_effect = lambda row, col: MagicMock(value="test_value")

        # This should not raise an exception
        try:
            form = ReadExpInfo("dummy_path.xlsx")
            self.assertIsInstance(form, ReadExpInfo)
        except Exception as e:
            self.fail(f"Base class instantiation failed: {e}")

    def test_msd_version_classes_importable(self):
        """Test that MSD version classes can be imported and are classes"""
        self.assertTrue(hasattr(ExpFormMsdV210305, '__bases__'))
        self.assertIn(ReadExpInfo, ExpFormMsdV210305.__bases__)

    def test_elisa_version_classes_importable(self):
        """Test that ELISA version classes can be imported and are classes"""
        self.assertTrue(hasattr(ExpFormElisaV201222, '__bases__'))
        self.assertIn(ReadExpInfo, ExpFormElisaV201222.__bases__)

    def test_form_classes_dict_structure(self):
        """Test that the FORM_CLASSES dictionary has expected structure"""
        from src.data_import.exp_reader import FORM_CLASSES

        # Should be a dictionary with (assay_type, version) keys
        self.assertIsInstance(FORM_CLASSES, dict)

        # Should have some MSD entries
        msd_keys = [k for k in FORM_CLASSES.keys() if k[0] == "MSD"]
        self.assertGreater(len(msd_keys), 0, "Should have MSD form classes")

        # Should have some ELISA entries
        elisa_keys = [k for k in FORM_CLASSES.keys() if k[0] == "ELISA"]
        self.assertGreater(len(elisa_keys), 0, "Should have ELISA form classes")

    def test_load_exp_form_with_invalid_params(self):
        """Test that load_exp_form raises appropriate error for invalid params"""
        with self.assertRaises(ValueError) as context:
            load_exp_form("dummy.xlsx", "INVALID", "v1.0")

        self.assertIn("No form class", str(context.exception))


if __name__ == '__main__':
    unittest.main()