"""
"""

from src.controllers.controller_utils import show_flow_title_and_descriptions, ask_a_choice, ask_for_string, ask_for_number, ask_yes_no

from src.qc.qc_lookup import fetch_ls_qc_lot_from_db, get_qc_details_by_lot_part_1, get_qc_details_by_lot_part_2


def lookup_qc_flow_by_lot(db_path):
    """
    The parent flow is qc_lookup_flow.
    """

    while True:

        show_flow_title_and_descriptions("Lookup QC by Lot Nº", 
                                         "Show QC details by selecting a Lot Nº.")
        


        # Ask user for the input TODO: Move this to a separate module?

        # 1) Ask for QC Lot Nº
        ls_qc_lot_numbers = fetch_ls_qc_lot_from_db(db_path) # TODO: Implement this function

        if len(ls_qc_lot_numbers) == 0: # TODO: We need to test this case
            print("No QC Lot Nº found in the database.")
            return "Back to QC Lookup Menu..."
        else:
            qc_lot_number = ask_a_choice("Select a QC Lot Nº", ls_qc_lot_numbers)



        # Review the selected options
        confirm_action = review_and_confirm_selections([qc_lot_number])

        if confirm_action == "fetch details":
            showing_qc_lookup_results(db_path, qc_lot_number) # TODO: Need a return value?
        elif confirm_action == "qc lookup menu":
            return confirm_action
        


        # Ask next step
        next_action = handle_next_step()
        if next_action == "restart":
            continue
        else:
            return next_action

def lookup_qc_flow_by_assay(db_path):
    """
    """
    while True:
        show_flow_title_and_descriptions("Lookup QC by Assay", 
                                         "Show QC details by selecting an Assay.")
        
        print("This functionality is not implemented yet.")

def lookup_qc_flow_by_analyte(db_path):
    """
    """
    while True:
        show_flow_title_and_descriptions("Lookup QC by Analyte", 
                                         "Show QC details by selecting an Analyte.")
        
        print("This functionality is not implemented yet.")


# TODO: Discard this function
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










def review_and_confirm_selections(selections:list) -> str:
    """
    selections: list. A list of selections to review.

    It's a helper function to review and confirm their selection.

    Returns a string indicating the next action.
    """

    # Review the selected options
    selections_str = " > ".join(selections)
    print(f"\nYou selected: {selections_str}")

    # Ask for confirmation before fetching details
    is_confirmed = ask_yes_no("Do you want to fetch the details for this QC Lot Nº?")
    if not is_confirmed:
        print("QC lookup cancelled.")
        print("Back to QC Lookup Menu...")
        return "qc lookup menu"
    else:
        print("Fetching QC details...")
        return "fetch details"


def showing_qc_lookup_results(db_path, qc_lot_number):
    """
    Show the results of the QC lookup.
    """
    details = get_qc_details_by_lot_part_1(db_path, qc_lot_number)

    if not details:
        print(f"No QC found with Lot Nº: {qc_lot_number}")
        return # TODO: Add safe exit
    
    # Extract common details from the first row
    lot_number, qc_name, qc_type, manufacturer, cat_number, expiration_date, preparation_date = details[0]
    
    # Print the common details
    print("QC Details:")
    print(f"\t- QC Name: {qc_name}")
    print(f"\t- Lot Number: {lot_number}")

    if qc_type == "Purchased":
        print(f"\t- Manufacturer: {manufacturer}")
        print(f"\t- Catalog Number: {cat_number}")
        print(f"\t- Expiration Date: {expiration_date}")
    elif qc_type == "Home made":
        print(f"\t- Preparation Date: {preparation_date}")
        



    # Part 2: Get analyte names and concentrations
    details = get_qc_details_by_lot_part_2(db_path, qc_lot_number)
    if details:
        print(f"\t- Concentration:")
        for analyte_name, concentration, unit in details:
            print(f"\t\t- {analyte_name}: {concentration} {unit}")
    else:
        print(f"No QC found with Lot Nº: {qc_lot_number}")
        return # TODO: Add safe exit
    
    
    print()



def handle_next_step() -> str:
    """
    It's a helper function to ask the user what they want to do next.
    """
    next_step = ask_a_choice("What do you want to do next?", 
                             ["Lookup another QC", "Back to QC Lookup Menu", "Back to Main Menu"])
    # TODO: Do we need "Back to QC Menu"?

    if next_step == "Lookup another QC":
        return "restart"
    elif next_step == "Back to QC Lookup Menu":
        return "qc lookup menu"
    elif next_step == "Back to Main Menu":
        return "main menu"