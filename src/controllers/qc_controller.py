# TODO: Discard this module after all functions are moved to the new module

import sqlite3

from src.controllers.controller_utils import ask_a_choice, ask_for_string, ask_for_number, ask_yes_no

from src.qc.qc_database import insert_qc, insert_qc_analyte


def fetch_manufacturers_from_db(db_path):
    """Fetch all manufacturer names from database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM manufacturer ORDER BY name")
    manufacturers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return manufacturers


def fetch_analytes_from_db(db_path):
    """Fetch all analyte names from database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM analyte ORDER BY name")
    analytes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return analytes


def fetch_units_from_db(db_path):
    """Fetch distinct units from qc_analyte table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT unit FROM qc_analyte ORDER BY unit")
    units = [row[0] for row in cursor.fetchall()]
    conn.close()
    # Add common units if not found in database
    common_units = ["pg/ml", "ng/ml", "µg/ml", "mg/ml"]
    for unit in common_units:
        if unit not in units:
            units.append(unit)
    return sorted(units)


def validate_date(date_str):
    """Validate date format YYYY-MM-DD."""
    if not date_str:
        return True  # None dates are allowed
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_qc_analyte_info(db_path, analytes_list):
    """Get analyte concentration information for QC."""
    analyte_and_conc = []
    
    print("\nEnter concentration information for each analyte:")
    
    for analyte_name in analytes_list:
        while True:
            try:
                conc = ask_for_number(f"Enter concentration for {analyte_name}")
                if conc >= 0:
                    break
                else:
                    print("Concentration must be non-negative.")
            except ValueError:
                print("Please enter a valid number.")
        
        analyte_and_conc.append((analyte_name, conc))
    
    return analyte_and_conc


# TODO: Move this function to a separate module
def add_qc_flow(db_path):
    """
    Flow for adding a QC.
    """
    print()
    print("Adding a QC...")
    
    # Get available options from database
    manufacturers = fetch_manufacturers_from_db(db_path)
    analytes = fetch_analytes_from_db(db_path)
    units = fetch_units_from_db(db_path)

    # Ask QC basic information
    qc_type = ask_a_choice("Select QC type", ["Purchased", "Home made"])

    if qc_type == "Purchased":
        if not manufacturers:
            print("No manufacturers found in database. Please add manufacturers first.")
            return
        
        manufacturer = ask_a_choice("Select manufacturer", manufacturers)
        qc_cat_number = ask_for_string("Enter QC Catalog Number")
        
        # QC Lot Number (UNIQUE)
        while True:
            qc_lot_number = ask_for_string("Enter QC Lot Number")
            if qc_lot_number.strip():
                break
            print("Lot number cannot be empty.")

        qc_name = ask_for_string("Enter QC name")
        
        unit = ask_a_choice("Select unit", units)
        
        # Expiration date
        while True:
            expiration_date = ask_for_string("Enter expiration date (YYYY-MM-DD) or leave empty")
            if not expiration_date or validate_date(expiration_date):
                break
            print("Invalid date format. Use YYYY-MM-DD or leave empty.")
        
        preparation_date = None
    
    elif qc_type == "Home made":
        manufacturer = None
        qc_cat_number = None

        # QC Lot Number (UNIQUE)
        while True:
            qc_lot_number = ask_for_string("Enter QC Lot Number")
            if qc_lot_number.strip():
                break
            print("Lot number cannot be empty.")

        qc_name = ask_for_string("Enter QC name")    

        unit = ask_a_choice("Select unit", units)
        
        expiration_date = None
        
        # Preparation date
        while True:
            preparation_date = ask_for_string("Enter preparation date (YYYY-MM-DD)")
            if validate_date(preparation_date):
                break
            print("Invalid date format. Use YYYY-MM-DD.")

    # Deal with analyte levels
    if not analytes:
        print("No analytes found in database. Please add analytes first.")
        return

    is_multiplex = ask_yes_no("Is this a multiplex QC?")
    
    if is_multiplex:
        print("Multiplex QC functionality is not implemented yet.")
        return  # TODO: Implement multiplex QC functionality
    else:
        # Single analyte QC
        analyte_name = ask_a_choice("Select analyte", analytes)
        analytes_list = [analyte_name]

    # Get concentration information
    analyte_and_conc = get_qc_analyte_info(db_path, analytes_list)

    # TODO: Link to assay? 
    # Probably in another many-to-many table to link QC to assay
    # Because QC could be used in different assays (e.g. MSD U-PLEX assays)
    print("Note: Linking QC to assay is not implemented yet.")

    # Preview the QC details
    print("\n" + "="*50)
    print("QC DETAILS PREVIEW")
    print("="*50)
    print(f"QC Type: {qc_type}")
    print(f"QC Name: {qc_name}")
    print(f"Lot Number: {qc_lot_number}")
    if manufacturer:
        print(f"Manufacturer: {manufacturer}")
    if qc_cat_number:
        print(f"Catalog Number: {qc_cat_number}")
    if preparation_date:
        print(f"Preparation Date: {preparation_date}")
    if expiration_date:
        print(f"Expiration Date: {expiration_date}")
    print("\nAnalyte Information:")
    for analyte_name, conc in analyte_and_conc:
        print(f"  - {analyte_name}: {conc} {unit}")
    print("="*50)

    # Ask for confirmation
    confirm = ask_yes_no("\nDo you want to add this QC to the database?")
    if confirm:
        try:
            # Insert QC
            qc_id = insert_qc(
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
            
            if qc_id is None:
                print("Failed to add QC (lot number may already exist).")
                return
            
            # Insert QC analytes
            for analyte_name, conc in analyte_and_conc:
                insert_qc_analyte(
                    db_path,
                    qc_id,  # Use qc_id instead of qc_lot_number
                    analyte_name,
                    conc,
                    unit
                )

            print("✅ QC added successfully!")
            print(f"QC ID: {qc_id}")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error adding QC: {e}")
            print("QC addition failed.")
    else:
        print("QC addition cancelled.")
        print("-" * 50)    

