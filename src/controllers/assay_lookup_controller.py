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

from src.controllers.messages_and_ask_questions import show_flow_title_and_descriptions

from src.assay_lookup.assay_lookup import (
    get_assay_details_by_name, get_analytes_for_assay,
    select_assay_name, select_species, select_assay_type_by_species, select_assay_by_species_and_type,
    select_analyte_for_species, select_assay_for_species_and_analyte
)







def assay_lookup_flow_details_full(db_path): # TODO: Combine it with showing_assay_results()?

    show_flow_title_and_descriptions("Assay Lookup - Full List", "...") # TODO: Add description

    # Ask user for the input TODO: Move this to a separate module?
    assay_name = select_assay_name(db_path)




    # Review the selected options

    # Show the results
    if assay_name:
        showing_assay_results(db_path, assay_name)

def showing_assay_results(db_path, assay_name:str): # TODO: Move this to let assay_lookup_flow functions stay together
    """
    This function obtains assay details using ONE assay name.

    The details are in 2 parts:
    1. Assay details (species, assay type, manufacture, kit catalog number, format)
    2. Analytes (with spot numbers) for the assay.

    It then displays the details in a user-friendly format.
    
    Combined function to let user select an assay and display all related details.
    Species, assay type, and manufacture are shown once.
    All kit catalog numbers and formats are shown.
    The analyte list (with spot numbers) for the assay is also shown.
    """
    # Part 1: Assay details
    # Obtain assay details using the assay name
    details = get_assay_details_by_name(db_path, assay_name)

    if not details:
        print(f"No details found for assay '{assay_name}'.")
        return

    # Extract common details from the first row
    first_row = details[0]
    _, species, assay_type, manufacture, _, _ = first_row




    # Show the details in a user-friendly format
    print(f"\nDetails for Assay: {assay_name}")
    print("-" * 50)
    print(f"Species: {species}")
    print(f"Assay Type: {assay_type}")
    print(f"Manufacture: {manufacture}")




    # Part 2: Analytes
    # Get and display analytes with spot numbers
    analytes = get_analytes_for_assay(db_path, assay_name)
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










def assay_lookup_flow_details_step_by_step(db_path):
    """
    Full interactive lookup - species -> assay type -> assay name -> show details.
    Uses new showing_assay_results() which now takes assay_name directly.
    """
    show_flow_title_and_descriptions("Assay Lookup - Step-by-Step Filter", "...") # TODO: Add description


    # Ask user for the input TODO: Move this to a separate module?
    species = select_species(db_path)
    if not species:
        return

    species_id, species_name = species

    assay_type = select_assay_type_by_species(db_path, species_id)
    if not assay_type:
        return

    assay_type_id, assay_type_name = assay_type

    assay = select_assay_by_species_and_type(db_path, species_id, assay_type_id)
    if not assay:
        return

    assay_id, assay_name = assay



    # Review the selected options
    print(f"\nYou selected: {species_name} > {assay_type_name} > {assay_name}")
    print("Fetching assay details...\n")


    # Show the results
    showing_assay_results(db_path, assay_name)  # Now takes `assay_name` directly











def assay_lookup_flow_details_by_species_and_analyte(db_path):
    """
    Use species and analyte to filter the assay list.
    Species + Analyte -> Assay -> Details
    Uses new showing_assay_results() which now takes assay_name directly.
    """
    show_flow_title_and_descriptions("Assay Lookup - Filter by Species and Analyte", 
                                     "Use Species and Analyte to filter the assay options.")


    # Ask user for the input 
        # TODO: I feel that I need to refactor the database schema to make this easier.
            # Remove assay_id from the kit table and create a assay_kits table to link kits to assays.
        # TODO: Move this to a separate module? or use the asking functions from messages_and_ask_questions.py?

        # Ask species:
            # - obtain species list from the database
            # - use ask_a_choice() to show the list and get the user's choice
            

    species = select_species(db_path)
    if not species:
        return # TODO: Add safe exit

    species_id, species_name = species

    analyte = select_analyte_for_species(db_path, species_id)
    if not analyte:
        return # TODO: Add safe exit

    analyte_id, analyte_name = analyte

    assay = select_assay_for_species_and_analyte(db_path, species_id, analyte_id)
    if not assay:
        return # TODO: Add safe exit

    _, assay_name = assay



    # Review the selected options
    print(f"\nYou selected: {species_name} > {analyte_name} > {assay_name}")
    # TODO: Add a confirmation step before fetching details


    print("Fetching assay details...\n")


    # Show the results
    showing_assay_results(db_path, assay_name) # TODO: Refactor this to do lookup and show results in different functions