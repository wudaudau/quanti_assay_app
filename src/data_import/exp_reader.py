"""
Reads Excel files (using your existing ExpInfoForm classes/functions)

Inputs: Excel path
Outputs: dictionary or DataFrames like:
{
    "form": {...},             # general exp info
    "sd_preparation": {...},   # sd7 info
    "sample_info": DataFrame,  # A01–H12 well data
    "readouts": DataFrame,     # same index, multiple analytes/wavelengths
}
"""

import pandas as pd
from typing import Optional, Dict, Any

from src.data_import.exp_forms.base import ReadExpInfo
from src.data_import.exp_forms.msd_versions.v210305 import ExpFormMsdV210305
from src.data_import.exp_forms.msd_versions.v210310 import ExpFormMsdV210310
from src.data_import.exp_forms.msd_versions.v211019 import ExpFormMsdV211019
from src.data_import.exp_forms.msd_versions.v220907 import ExpFormMsdV220907
from src.data_import.exp_forms.msd_versions.v230306 import ExpFormMsdV230306
from src.data_import.exp_forms.msd_versions.v240104 import ExpFormMsdV240104
from src.data_import.exp_forms.msd_versions.v250227 import ExpFormMsdV250227
from src.data_import.exp_forms.elisa_versions.v201222 import ExpFormElisaV201222
from src.data_import.exp_forms.elisa_versions.v210310 import ExpFormElisaV210310
from src.data_import.exp_forms.elisa_versions.v230228 import ExpFormElisaV230228
from src.data_import.exp_forms.elisa_versions.v250227 import ExpFormElisaV250227
from src.database.exp_logging_db import log_experiment_from_form


FORM_CLASSES = {
    ("MSD", None): ExpFormMsdV210310,  # Default to the latest version
    ("MSD", "v20210305"): ExpFormMsdV210305,
    ("MSD", "v20210310"): ExpFormMsdV210310,
    ("MSD", "v20211019"): ExpFormMsdV211019,
    ("MSD", "v20220907"): ExpFormMsdV220907,
    ("MSD", "v20230306"): ExpFormMsdV230306,
    ("MSD", "v20240104"): ExpFormMsdV240104,
    ("MSD", "v20250227"): ExpFormMsdV250227,
    ("ELISA", None): ExpFormElisaV201222,  # Default to the latest version
    ("ELISA", "v20201222"): ExpFormElisaV201222,
    ("ELISA", "v20210310"): ExpFormElisaV210310,
    ("ELISA", "v20230228"): ExpFormElisaV230228,
    ("ELISA", "v20250227"): ExpFormElisaV250227,
}


def load_exp_form(file_path, assay_type=None, form_version=None):
    key = (assay_type, form_version)
    form_class = FORM_CLASSES.get(key)

    if form_class is None:
        raise ValueError(f"No form class for assay_type={key[0]}, form_version={key[1]}")

    return form_class(file_path)


def extract_exp_data(form):
    """Returns all extracted data from the form as a dict."""
    return {
        "exp_log": {
            "exp_date": form.expdate,
            "species": form.species,
            "assay_type": form.assay_type,
            "assay_name": form.assay_name,
            "sample_type": form.sampletype,
            "manipulator_1": form.manipulator_1,
            "manipulator_2": form.manipulator_2,
            "manipulator_3": form.manipulator_3,
            "project_name": form.project_name,
            "cohort_name": form.cohort,
            "plate_layout_name": form.expinfo,
            "plate_bar_code": form.plate_bar_code,
            "kit_cat_number": form.kitcat,
            "sd_cat_number": form.sdcat,
            "sd_lot_number": form.sdlots, # This should be a list of lot numbers. Some MSD assays have multiple lot numbers.
            "qc_h_lot_number": form.qchlot,
            "qc_m_lot_number": form.qcmlot,
            "qc_l_lot_number": form.qcllot,
            "notes": form.exp_note,
        },
        "sd_preparation": {
            "sd7_concentration": form.sd7_dilu_factor,
            "serial_dilution_factor": form.sd_serial_dilu_factor,
        },
        "well_data": form.sample_info_df,
        "readouts": getattr(form, "readout_df", None),  # Optional for MSD
    }


def log_experiment_from_excel(db_path: str, excel_path: str, assay_type: Optional[str] = None, form_version: Optional[str] = None) -> int:
    """
    Load an Excel file, extract experiment data, and log it to the database.

    Args:
        db_path: Path to the SQLite database
        excel_path: Path to the Excel file to process
        assay_type: Type of assay ("MSD" or "ELISA") - auto-detected if None
        form_version: Specific form version - uses latest if None

    Returns:
        int: The ID of the logged experiment

    Raises:
        ValueError: If form cannot be loaded or data extraction fails
        Exception: If database insertion fails
    """
    # Load the appropriate form class
    form = load_exp_form(excel_path, assay_type, form_version)

    # Extract data from the form
    extracted_data = extract_exp_data(form)

    # Transform extracted data to database format
    db_data = transform_extracted_data_to_db_format(extracted_data)

    # Log to database
    experiment_id = log_experiment_from_form(db_path, db_data)

    return experiment_id


def transform_extracted_data_to_db_format(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform the extracted data from exp_reader format to database format.

    Args:
        extracted_data: Data from extract_exp_data()

    Returns:
        Dict formatted for log_experiment_from_form()
    """
    exp_log = extracted_data["exp_log"]

    # Handle SD lot numbers - if it's a list, take the first one or join them
    sd_lot = exp_log.get("sd_lot_number")
    if isinstance(sd_lot, list):
        sd_lot = sd_lot[0] if sd_lot else None

    # Build the database-formatted data
    db_data = {
        "exp_date": exp_log["exp_date"],
        "species": exp_log["species"],
        "assay_type": exp_log["assay_type"],
        "assay_name": exp_log["assay_name"],
        "sample_type": exp_log["sample_type"],
        "manipulator_1": exp_log["manipulator_1"],
        "manipulator_2": exp_log.get("manipulator_2"),
        "manipulator_3": exp_log.get("manipulator_3"),
        "project_name": exp_log.get("project_name"),
        "cohort_name": exp_log.get("cohort_name"),
        "plate_layout_name": exp_log.get("plate_layout_name"),
        "plate_bar_code": exp_log.get("plate_bar_code"),
        "kit_cat_number": exp_log["kit_cat_number"],
        "sd_cat_number": exp_log.get("sd_cat_number"),
        "sd_lot_number": sd_lot,
        "qc_h_lot_number": exp_log.get("qc_h_lot_number"),
        "qc_m_lot_number": exp_log.get("qc_m_lot_number"),
        "qc_l_lot_number": exp_log.get("qc_l_lot_number"),
        "notes": exp_log.get("notes"),
    }

    # Add SD preparation data if available
    sd_prep = extracted_data.get("sd_preparation", {})
    if sd_prep.get("sd7_concentration") or sd_prep.get("serial_dilution_factor"):
        db_data["sd_preparation"] = {
            "sd7_concentration": sd_prep.get("sd7_concentration"),
            "serial_dilution_factor": sd_prep.get("serial_dilution_factor"),
            "sd7_unit": "pg/mL"  # Default unit, could be made configurable
        }

    # Transform well data from DataFrame to list of dicts
    well_df = extracted_data.get("well_data")
    if well_df is not None and not well_df.empty:
        well_data = []
        for idx, row in well_df.iterrows():
            well_data.append({
                "well_id": idx,  # Assuming index is well ID like 'A01'
                "sample_name": row.get("sample_name"),
                "sample_role": row.get("sample_role", "unknown"),
                "dilution_factor": row.get("dilution_factor"),
                "freeze_thaw_cycle": row.get("freeze_thaw_cycle"),
                "excluded": row.get("excluded", False)
            })
        db_data["well_data"] = well_data

    # Transform readout data if available
    readout_df = extracted_data.get("readouts")
    if readout_df is not None and not readout_df.empty:
        readout_data = {}
        # Transform from DataFrame format to the expected dict format
        # This will need to be adapted based on the actual DataFrame structure
        for well_id in readout_df.index:
            well_readouts = []
            for analyte in readout_df.columns:
                if pd.notna(readout_df.loc[well_id, analyte]):
                    well_readouts.append({
                        "analyte_name": analyte,
                        "value": readout_df.loc[well_id, analyte],
                        "readout_type": "raw"  # Default type
                    })
            if well_readouts:
                readout_data[well_id] = well_readouts

        if readout_data:
            db_data["readout_data"] = readout_data

    return db_data



