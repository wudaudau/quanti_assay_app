"""
This module provides functions to interact with the assay lookup database.

There are currently three lookup methods (basic into)
TODO: Move to a separate module: assay_lookup/basic_info.py


TODO: Add more Assay Lookup functions
- [ ] assay_lookup/reagent_info.py
- [ ] assay_lookup/steps_overview.py
- [ ] assay_lookup/protocols.py
- [ ] assay_lookup/sds_info.py


"""

from src.controllers.controller_utils import show_flow_title_and_descriptions, ask_a_choice, ask_yes_no

# from src.controllers.assay_menu_controller import assay_menu_flow
# from src.controllers.main_menu_controller import main_menu_flow

from src.assay_lookup.assay_lookup import (
    get_assay_details_part_1, get_assay_details_part_2, # TODO: Redundant function?
    fetch_ls_assays_from_db, 
    fetch_ls_species_from_db, fetch_ls_assay_types_from_db_based_on_species, fetch_ls_assays_from_db_based_on_species_and_assay_type,
    fetch_ls_analytes_from_db_based_on_species, fetch_ls_assays_from_db_based_on_species_and_analyte
)







def assay_lookup_flow_no_filter(db_path): # TODO: Combine it with showing_assay_results()?
    """
    The parent flow is assay_menu_flow().
    """

    while True:

        show_flow_title_and_descriptions("Lookup Assay (No Filter)", 
                                         "Show assay details by selecting an assay name.")

        # Ask user for the input TODO: Move this to a separate module?

        # 1) Ask an assay name:
            # Obtain the list of assay names from the database
            # Use ask_a_choice() to show the list and get the user's choice
        ls_assays = fetch_ls_assays_from_db(db_path)

        if len(ls_assays) == 0: # TODO: We need to test this case
            print("No assays found in the database.")
            print("Back to the Assay Menu...")
            return "assay menu" # Back to assay_menu_flow()
        else:
            assay_name = ask_a_choice("\nAvailable Assays:", ls_assays)

        

        # Review the selected options
        confirm_action = review_and_confirm_selections([assay_name])

        if confirm_action == "fetch details":
            showing_assay_results(db_path, assay_name) # TODO: Need a return value?
        elif confirm_action == "assay menu":
            return confirm_action


        # Ask next step
        next_action = handle_next_step()
        if next_action == "restart":
            continue
        else:
            return next_action # Return to the caller function (assay_menu_flow() or main_menu_flow())



def assay_lookup_flow_filter_by_species_and_assay_type(db_path):
    """
    Full interactive lookup - species -> assay type -> assay name -> show details.
    Uses new showing_assay_results() which now takes assay_name directly.
    """

    while True:
        show_flow_title_and_descriptions("Lookup Assay (Filter by Species and Assay Type)", 
                                        "Use Species and Assay Type to filter the assay options.")


        # Ask user for the input TODO: Move this to a separate module?

        # 1) Ask species:
            # Obtain species list from the database
            # Use ask_a_choice() to show the list and get the user's choice
        ls_species = fetch_ls_species_from_db(db_path)
        if len(ls_species) == 0: # TODO: We need to test this case
            print("No species found in the database.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            species_name = ask_a_choice("\nAvailable Species:", ls_species)


        # 2) Ask assay type:
        ls_assay_type = fetch_ls_assay_types_from_db_based_on_species(db_path, species_name)
        if len(ls_assay_type) == 0: # TODO: We need to test this case
            print("No assay types found for this species.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            assay_type = ask_a_choice("\nAvailable Assay Types:", ls_assay_type)

        
        # 3) Ask assay name:
        ls_assays = fetch_ls_assays_from_db_based_on_species_and_assay_type(db_path, species_name, assay_type)
        if len(ls_assays) == 0: # TODO: We need to test this case
            print("No assays found for this species and assay type.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            assay_name = ask_a_choice("\nAvailable Assays:", ls_assays)
        



        # Review the selected options
        confirm_action = review_and_confirm_selections([species_name, assay_type, assay_name])
        
        if confirm_action == "fetch details":
            showing_assay_results(db_path, assay_name)
        elif confirm_action == "assay menu":
            return confirm_action


        # Ask next step
        next_action = handle_next_step()
        if next_action == "restart":
            continue
        else:
            return next_action # Return to the caller function (assay_menu_flow() or main_menu_flow())

def assay_lookup_flow_filter_by_species_and_analyte(db_path):
    """
    Use species and analyte to filter the assay list.
    Species + Analyte -> Assay -> Details
    Uses new showing_assay_results() which now takes assay_name directly.
    """

    while True:
        show_flow_title_and_descriptions("Lookup Assay (Filter by Species and Analyte)", 
                                        "Use Species and Analyte to filter the assay options.")


        # Ask user for the input TODO: Move this to a separate module?

        # 1) Ask species:
            # Obtain species list from the database
            # Use ask_a_choice() to show the list and get the user's choice
        ls_species = fetch_ls_species_from_db(db_path)
        if len(ls_species) == 0: # TODO: We need to test this case
            print("No species found in the database.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            species_name = ask_a_choice("\nAvailable Species:", ls_species)



        # 2) Ask analyte:
        ls_analytes = fetch_ls_analytes_from_db_based_on_species(db_path, species_name)
        if len(ls_analytes) == 0: # TODO: We need to test this case
            print("No analytes found for this species.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            analyte_name = ask_a_choice("\nAvailable Analytes:", ls_analytes)
        
        # 3) Ask assay name:
        ls_assays = fetch_ls_assays_from_db_based_on_species_and_analyte(db_path, species_name, analyte_name)
        if len(ls_assays) == 0:
            print("No assays found for this species and analyte.")
            print("Back to the Assay Menu...")
            return "assay menu"
        else:
            assay_name = ask_a_choice("\nAvailable Assays:", ls_assays)

        



        # Review the selected options
        confirm_action = review_and_confirm_selections([species_name, analyte_name, assay_name])

        if confirm_action == "fetch details":
            showing_assay_results(db_path, assay_name)
        elif confirm_action == "assay menu":
            return confirm_action



        # Ask next step
        next_action = handle_next_step()
        if next_action == "restart":
            continue
        else:
            return next_action # Return to the caller function (assay_menu_flow() or main_menu_flow())












def showing_assay_results(db_path, assay_name:str): # TODO: Move this to let assay_lookup_flow functions stay together
    """
    This function obtains assay details using ONE assay name.

    The details are in 2 parts:
    1. Assay details (species, assay type, manufacturer, kit catalog number, format)
    2. Analytes (with spot numbers) for the assay.

    It then displays the details in a user-friendly format.
    
    Combined function to let user select an assay and display all related details.
    Species, assay type, and manufacturer are shown once.
    All kit catalog numbers and formats are shown.
    The analyte list (with spot numbers) for the assay is also shown.
    """
    # Part 1: Assay details
    # Obtain assay details using the assay name
    details = get_assay_details_part_1(db_path, assay_name)

    if not details:
        print(f"No details found for assay '{assay_name}'.")
        return # TODO: Add safe exit

    # Extract common details from the first row
    first_row = details[0]
    _, species, assay_type, manufacturer, _, _ = first_row




    # Show the details in a user-friendly format
    print(f"\nDetails for Assay: {assay_name}")
    print("-" * 50)
    print(f"Species: {species}")
    print(f"Assay Type: {assay_type}")
    print(f"Manufacturer: {manufacturer}")




    # Part 2: Analytes
    # Get and display analytes with spot numbers
    analytes = get_assay_details_part_2(db_path, assay_name)
    if analytes:
        print("\nAnalytes (with spot numbers):")
        for analyte_name, spot_number in analytes:
            print(f"  - {analyte_name} (Spot {spot_number})")
    else:
        print("\nNo analytes found for this assay.")

    # List available kits
    print("\nAvailable Kits:")
    for _, _, _, _, kit_cat_number, kit_format in details:
        print(f"  - Catalog #: {kit_cat_number}, Format: {kit_format}")

    print("-" * 50)
    print()

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
    is_confirmed = ask_yes_no("Do you want to fetch the details for this assay?")
    if not is_confirmed:
        print("Assay details fetching cancelled.")
        print("Back to the Assay Menu...")
        return "assay menu" # Back to assay_menu_flow()
    else:
        print("Fetching assay details...\n")
        return "fetch details" # Proceed to fetch details


def handle_next_step() -> str:
    """
    It's a helper function to ask the user what they want to do next.
    """
    next_step = ask_a_choice("What do you want to do next?", 
                             ["Start a new assay lookup", "Go back to the Assay Mene", "Go back to the Main Mene"])
    
    if next_step == "Start a new assay lookup":
        return "restart" # Restart the loop
    elif next_step == "Go back to the Assay Mene":
        return "assay menu" # Back to assay_menu_flow() to restart the assay lookup
    elif next_step == "Go back to the Main Mene":
        return "main menu" # Back to assay_menu_flow() to go main menu (main menu)









