# TODO: Discard this module after all functions are moved to the new module

from src.controllers.controller_utils import ask_a_choice, ask_for_string, ask_for_number, ask_yes_no

from src.qc.qc_database import insert_qc, insert_qc_analyte


# TODO: Move this function to a separate module
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
        expiration_date = ask_for_string("Enter expiration date (YYYY-MM-DD)") # TODO: None is ok here?
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
    print(f"- QC Type: {qc_type}")
    print(f"- Manufacturer: {manufacturer}")
    print(f"- QC Cat Nº: {qc_cat_number}")
    print(f"- QC Lot Nº: {qc_lot_number}")
    print(f"- QC Name: {qc_name}")
    print(f"- Expiration Date: {expiration_date}")
    print(f"- Preparation Date: {preparation_date}")
    print()
    print("QC concentration details:")
    for analyte_name, conc in analyte_and_conc:
        print(f"\t- {analyte_name}\t {conc} {unit}")
    print()

    
    

    print()
    # Ask for confirmation
    confirm = ask_yes_no("Do you want to add this QC?")
    if confirm:
        insert_qc(
            db_path,
            qc_type,
            qc_name,
            qc_lot_number,
            manufacturer,
            qc_cat_number,
            unit,
            expiration_date,
            preparation_date
        )

        for analyte_name, conc in analyte_and_conc:
            insert_qc_analyte(
                db_path,
                qc_lot_number,
                analyte_name,
                conc,
                unit
            )

        print("QC added successfully!")
        print("-" * 50)
    else:
        print("QC addition cancelled.")
        print("-" * 50)
    
    

