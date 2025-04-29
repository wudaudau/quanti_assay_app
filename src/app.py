"""
This file manages the main loop and application flow.

"""


# create db and import data
import os
from src.database.db_core import create_database
from src.database.db_data_loader import load_all_data_from_csv


# Call main controller
from src.controllers.main_menu_controller import main_menu_flow









def run_app():

    # Database setup
    db_path = os.path.join("data", "quanti_assay.sqlite") # Path to the SQLite database file
    create_database(db_path)
    load_all_data_from_csv(db_path)



    show_welcome()
    main_menu_flow(db_path)
    show_goodbye()

