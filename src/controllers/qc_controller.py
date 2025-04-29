
from src.controllers.messages_and_ask_questions import ask_a_choice, ask_for_string, ask_for_number, ask_yes_no

from src.qc.qc_database import insert_qc

from src.qc.qc_lookup import get_qc_details_by_lot

def add_qc_flow(db_path):
    """
    Flow for adding a QC.
    """
    print()
    print("Adding a QC...")
    # Implement the logic to add a QC here



    # Ask QC basic information

    qc_type = ask_a_choice("Select QC type", ["Purchased", "Home made"])

    if qc_type == "Purchased":
        manufacturer = ask_a_choice("Select manufacturer", ["Manufacturer A", "Manufacturer B"]) # TODO: obtain list of manufacturers from the database
        qc_cat_number = ask_for_string("Enter QC Cat Nº")

        # QC Lot Nº (UNIQUE)
        qc_lot_number = ask_for_string("Enter QC Lot Nº")

        qc_name = ask_for_string("Enter QC name")

        unit = ask_a_choice("Select unit", ["pg/ml", "ng/ml"]) # TODO: obtain list of units from the database
        expiration_date = ask_for_string("Enter expiration date (YYYY-MM-DD)") # TODO: Validate date format
        preparation_date = None
    
    elif qc_type == "Home made":
        manufacturer = None
        qc_cat_number = None

        # QC Lot Nº (UNIQUE) # TODO: Need a convention for this
        qc_lot_number = ask_for_string("Enter QC Lot Nº")    

        qc_name = ask_for_string("Enter QC name")    

        unit = ask_a_choice("Select unit", ["pg/ml", "ng/ml"]) # TODO: obtain list of units from the database
        expiration_date = None
        preparation_date = ask_for_string("Enter preparation date (YYYY-MM-DD)") # TODO: Validate date format





    # Deal with analyte levels and 
        # One QC can have multiple analytes

    is_multiplex = ask_yes_no("Is this a multiplex QC?") 
    if is_multiplex:
        print("Multiplex QC functionality is not implemented yet.")
        
        # TODO: Develop multiplex QC functionality
        anlyte_count = ask_for_number("Enter number of analytes")
    else:
        anlyte_count = 1

    analyte_and_conc = []
    for i in range(anlyte_count):
        analyte_name = ask_a_choice(f"Select analyte name for analyte {i+1}", ["Analyte A", "Analyte B", "Analyte C", "Analyte D"]) # TODO: obtain list of analytes from the database
        conc = ask_for_number("Enter concentration")
    
        analyte_and_conc.append((analyte_name, conc))
    


    # TODO: Link to assay? 
        # Probably in another many-to-many table to link QC to assay
        # Because QC could be used in different assays (e.g. MSD U-PLEX assays)

    print("Linking QC to assay is not implemented yet.")
    



    # Preview the QC details
    print("\nQC Details:")
    print(f"\t- QC Type: {qc_type}")
    print(f"\t- Manufacturer: {manufacturer}")
    print(f"\t- QC Cat Nº: {qc_cat_number}")
    print(f"\t- QC Lot Nº: {qc_lot_number}")
    print(f"\t- QC Name: {qc_name}")
    print()
    print("\tQC concentration details:")
    for analyte_name, conc in analyte_and_conc:
        print(f"\t\t- {analyte_name}\t {conc} {unit}")
    print()

    
    print(f"\t- Expiration Date: {expiration_date}")
    print(f"\t- Preparation Date: {preparation_date}")

    print()
    # Ask for confirmation
    confirm = ask_yes_no("Do you want to add this QC?")
    if confirm:
        for analyte_name, conc in analyte_and_conc:
            insert_qc(
                db_path,
                qc_type,
                qc_name,
                qc_lot_number,
                manufacturer,
                qc_cat_number,
                unit,
                expiration_date,
                preparation_date,
                [(analyte_name, conc)]
            )
        print("QC added successfully!")
        print("-" * 50)
    else:
        print("QC addition cancelled.")
        print("-" * 50)
    
    

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