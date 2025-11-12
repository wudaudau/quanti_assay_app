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



