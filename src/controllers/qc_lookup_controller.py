"""
"""

from src.controllers.controller_utils import ask_a_choice, ask_for_string, ask_for_number, ask_yes_no

from src.qc.qc_lookup import get_qc_details_by_lot


def lookup_qc_flow(db_path):
    """
    Flow for looking up a QC.
    """
    print()
    print("Looking up a QC...")

    lookup_option = ask_a_choice("Select lookup option", ["By QC Lot Nº", "By Assay", "By Analyte"])
    if lookup_option == "By QC Lot Nº":
        qc_lot_number = ask_for_string("Enter QC Lot Nº")
        print()
        # Implement logic to look up QC by lot number
        print(f"Looking up QC with Lot Nº: {qc_lot_number}")
        results = get_qc_details_by_lot(db_path, qc_lot_number)
        print("QC Details:")
        for result in results:
            print(f"\t- QC Name: {result[0]}")
            print(f"\t- Lot Number: {result[1]}")
            print(f"\t- Catalog Number: {result[2]}")
            print(f"\t- Expiration Date: {result[3]}")
            print(f"\t- Preparation Date: {result[4]}")
            print(f"\t- Manufacturer Name: {result[5]}")
            print(f"\t- Analyte Name: {result[6]}")
            print(f"\t- Concentration: {result[7]}")
            print(f"\t- Unit: {result[8]}")
        if not results:
            print(f"No QC found with Lot Nº: {qc_lot_number}")
        print()
    elif lookup_option == "By Assay":
        assay_name = ask_for_string("Enter Assay name")
        # Implement logic to look up QC by assay name
        print(f"Looking up QC for Assay: {assay_name}")
        print("This functionality is not implemented yet.")
    elif lookup_option == "By Analyte":
        analyte_name = ask_for_string("Enter Analyte name")
        # Implement logic to look up QC by analyte name
        print(f"Looking up QC for Analyte: {analyte_name}")
        print("This functionality is not implemented yet.")
    # Implement the logic to look up a QC here
    # For example, you can call the lookup_qc function from the qc_controller module
    # and pass the necessary parameters.
    # Example:
    # lookup_qc(db_path, ...)
    print("QC lookup completed!")
    print("-" * 50)