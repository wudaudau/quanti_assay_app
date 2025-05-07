"""
Test src/data_import.
Test script to log an experiment into the SQLite database.
"""

import sqlite3
from src.data_import.exp_reader import load_exp_form, extract_exp_data
from src.data_import.exp_logger import insert_experiment

def main():
    db_path = "data/quanti_assay.sqlite"  # change if needed
    assay_type = "ELISA"  # change if needed
    form_version = "v20250227"  # change if needed
    excel_path = "/Users/wudaudau/Library/CloudStorage/OneDrive-UPEC/02_Exp Library/05_DataProcessQuanti/Quanti process files by batch (since 202401)(to be rearrange)/202503_AIMS CANDY/01_before data process/exp20250319_Pl1_AIMSCANDY_B2M_ExpInfoForm(ELISA)v20250227.xlsx"  # use your actual test file

    conn = sqlite3.connect(db_path)

    form = load_exp_form(excel_path, assay_type=assay_type, form_version=form_version)
    exp_data = extract_exp_data(form)
    exp_id = insert_experiment(conn, exp_data)

    print("Successfully inserted experiment with ID:", exp_id)

if __name__ == "__main__":
    main()