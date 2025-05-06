"""
This is the glue that connects the experiment logging process with the database.
It handles the insertion of experiment data into the database.
"""

import sqlite3
from typing import Dict, List


def insert_experiment(conn: sqlite3.Connection, exp_data: Dict) -> int:
    cur = conn.cursor()

    # --- Insert into exp_log ---
    log_data = exp_data["exp_log"]
        
    cur.execute("""INSERT INTO experiment_raw (
            exp_date, species, assay_type, assay_name, sample_type, 
            manipulator_1, manipulator_2, manipulator_3,
            project_name, cohort_name, plate_layout_name, plate_bar_code, 
            kit_cat_number, sd_cat_number,
            sd_lot_number, qc_h_lot_number, qc_m_lot_number, qc_l_lot_number,
            notes
        ) VALUES (?, ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?,
            ?, ?, ?, ?,
            ?
        )
    """, (
        log_data["exp_date"],
        log_data["species"],
        log_data["assay_type"],
        log_data["assay_name"],
        log_data["sample_type"],
        log_data.get("manipulator_1"),
        log_data.get("manipulator_2"),
        log_data.get("manipulator_3"),
        log_data.get("project_name"),
        log_data.get("cohort_name"),
        log_data.get("plate_layout_name"),
        log_data.get("plate_bar_code"),
        log_data["kit_cat_number"],
        log_data["sd_cat_number"],
        ", ".join(log_data["sd_lot_number"]) if isinstance(log_data["sd_lot_number"], list) else log_data["sd_lot_number"],
        log_data.get("qc_h_lot_number"),
        log_data.get("qc_m_lot_number"),
        log_data.get("qc_l_lot_number"),
        log_data.get("notes"),
    ))

    experiment_id = cur.lastrowid

    # --- Insert well_data ---
    for well_id, row in exp_data["well_data"].iterrows():
        cur.execute("""
            INSERT INTO well_data (
                experiment_id, well_id, sample_name, sample_role,
                dilution_factor, freeze_thaw_cycle, excluded
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            experiment_id,
            well_id,
            row["sample_name"],
            row["sample_role"],
            row["dilution_factor"],
            row.get("freeze_thraw_cycle"),
            bool(row.get("excluded", False)),
        ))
        row["_db_id"] = cur.lastrowid  # Save it in case needed later

    # --- Insert readouts ---
    if exp_data["readouts"] is not None:
        for _, row in exp_data["readouts"].iterrows():
            cur.execute("""
                INSERT INTO readouts (
                    well_data_id, analyte_name, value, unit
                ) VALUES (?, ?, ?, ?)
            """, (
                get_well_id_by_label(exp_data["well_data"], row["Well"]),
                row["Analyte"],  # could be analyte_name or wavelength
                row["value"],
                row.get("unit", None),
            ))

    # --- Insert sd_preparation ---
    sd_prep = exp_data.get("sd_preparation", {})
    if sd_prep:
        cur.execute("""
            INSERT INTO sd_preparation (
                experiment_id, sd7_concentration, serial_dilution_factor
            ) VALUES (?, ?, ?)
        """, (
            experiment_id,
            str(sd_prep.get("sd7_concentration")),  # Often a dict
            sd_prep.get("serial_dilution_factor"),
        ))

    conn.commit()
    return experiment_id


def get_well_id_by_label(well_df, label):
    """Utility to map 'A01' back to the DB ID if needed."""
    try:
        return well_df.loc[label, "_db_id"]
    except KeyError:
        raise ValueError(f"Well '{label}' not found in well_data DataFrame")