
from src.controllers.messages_and_ask_questions import ask_a_choice

def add_qc_flow(db_path):
    """
    Flow for adding a QC.
    """
    print("Adding a QC...")
    # Implement the logic to add a QC here

    qc_type = ask_a_choice("Select QC type", ["Purchased", "Home made"])

    if qc_type == "Purchased":
        # Manufacture
        # QC Cat Nº
        # QC Lot Nº (UNIQUE)
        # QC name
        # Analyte name
        # concentration
        # Expiration date
        # unit

        # TODO: Link to assay? 
            # Probably in another many-to-many table to link QC to assay
            # Because QC could be used in different assays (e.g. MSD U-PLEX assays)
        pass
    elif qc_type == "Home made":
        # QC Lot Nº (UNIQUE) # TODO: Need a convention for this
        # QC name
        # Analyte name
        # concentration
        # Preparation date
        pass

    # Ask the lot Nº
    lot_number = input("Enter the lot number: ").strip()

    # Check if the lot Nº is existing
    # Implement the logic to check if the lot number exists in the database

    # For example, you can call the add_qc function from the qc_controller module
    # and pass the necessary parameters.
    # Example:
    # add_qc(db_path, ...)
    print("QC added successfully!")

def lookup_qc_flow(db_path):
    """
    Flow for looking up a QC.
    """
    print("Looking up a QC...")
    # Implement the logic to look up a QC here
    # For example, you can call the lookup_qc function from the qc_controller module
    # and pass the necessary parameters.
    # Example:
    # lookup_qc(db_path, ...)
    print("QC lookup completed!")