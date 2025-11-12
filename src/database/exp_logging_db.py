"""
Database functions for experiment logging - handles insertion into experiment_raw and related tables
"""

import sqlite3
from typing import Dict, List, Optional, Any
from datetime import datetime
from src.database.db_utils import get_or_insert


def insert_experiment_raw(cursor, experiment_data: Dict[str, Any]) -> int:
    """
    Insert experiment metadata into experiment_raw table.

    Args:
        cursor: SQLite cursor
        experiment_data: Dict containing experiment metadata

    Returns:
        int: The ID of the inserted experiment_raw record
    """
    required_fields = [
        'exp_date', 'species', 'assay_type', 'assay_name', 'sample_type',
        'manipulator_1', 'kit_cat_number'
    ]

    # Check required fields
    for field in required_fields:
        if field not in experiment_data:
            raise ValueError(f"Missing required field: {field}")

    # Prepare data with defaults for optional fields
    data = {
        'exp_date': experiment_data['exp_date'],
        'species': experiment_data['species'],
        'assay_type': experiment_data['assay_type'],
        'assay_name': experiment_data['assay_name'],
        'sample_type': experiment_data['sample_type'],
        'manipulator_1': experiment_data['manipulator_1'],
        'manipulator_2': experiment_data.get('manipulator_2'),
        'manipulator_3': experiment_data.get('manipulator_3'),
        'project_name': experiment_data.get('project_name'),
        'cohort_name': experiment_data.get('cohort_name'),
        'plate_layout_name': experiment_data.get('plate_layout_name'),
        'plate_bar_code': experiment_data.get('plate_bar_code'),
        'kit_cat_number': experiment_data['kit_cat_number'],
        'sd_cat_number': experiment_data.get('sd_cat_number'),
        'sd_lot_number': experiment_data.get('sd_lot_number'),
        'qc_h_lot_number': experiment_data.get('qc_h_lot_number'),
        'qc_m_lot_number': experiment_data.get('qc_m_lot_number'),
        'qc_l_lot_number': experiment_data.get('qc_l_lot_number'),
        'notes': experiment_data.get('notes')
    }

    # Convert dict to ordered values for SQL
    columns = list(data.keys())
    values = [data[col] for col in columns]
    placeholders = ','.join(['?' for _ in columns])

    query = f"""
    INSERT INTO experiment_raw ({','.join(columns)})
    VALUES ({placeholders})
    """

    cursor.execute(query, values)
    return cursor.lastrowid


def insert_well_data(cursor, experiment_raw_id: int, well_data: List[Dict[str, Any]]) -> List[int]:
    """
    Insert well data for an experiment.

    Args:
        cursor: SQLite cursor
        experiment_raw_id: ID of the parent experiment_raw record
        well_data: List of dicts containing well information

    Returns:
        List[int]: IDs of inserted well_data records
    """
    well_ids = []

    for well in well_data:
        data = {
            'experiment_raw_id': experiment_raw_id,
            'well_id': well['well_id'],
            'sample_name': well.get('sample_name'),
            'sample_role': well.get('sample_role'),
            'dilution_factor': well.get('dilution_factor'),
            'freeze_thaw_cycle': well.get('freeze_thaw_cycle'),
            'excluded': well.get('excluded', False)
        }

        well_id = get_or_insert(cursor, 'well_data', data)
        well_ids.append(well_id)

    return well_ids


def insert_readouts(cursor, well_data_ids: List[int], readout_data: Dict[str, List[Dict[str, Any]]]) -> List[int]:
    """
    Insert readout data for wells.

    Args:
        cursor: SQLite cursor
        well_data_ids: List of well_data IDs
        readout_data: Dict mapping well_ids to list of readout records

    Returns:
        List[int]: IDs of inserted readout records
    """
    readout_ids = []

    for well_data_id in well_data_ids:
        # Find corresponding readout data (this would need to be matched by well_id)
        # For now, assuming readout_data is structured as {well_id: [readout_records]}
        well_id = None  # TODO: Need to get well_id from well_data_id

        if well_id in readout_data:
            for readout in readout_data[well_id]:
                data = {
                    'well_data_id': well_data_id,
                    'analyte_name': readout['analyte_name'],
                    'value': readout.get('value'),
                    'readout_type': readout.get('readout_type', 'raw')
                }

                readout_id = get_or_insert(cursor, 'readout', data)
                readout_ids.append(readout_id)

    return readout_ids


def insert_sd_preparation(cursor, experiment_raw_id: int, sd_data: Dict[str, Any]) -> Optional[int]:
    """
    Insert standard preparation data for an experiment.

    Args:
        cursor: SQLite cursor
        experiment_raw_id: ID of the parent experiment_raw record
        sd_data: Dict containing SD preparation information

    Returns:
        Optional[int]: ID of inserted sd_preparation record, or None if no data
    """
    if not sd_data:
        return None

    data = {
        'experiment_raw_id': experiment_raw_id,
        'sd7_concentration': sd_data.get('sd7_concentration'),
        'serial_dilution_factor': sd_data.get('serial_dilution_factor'),
        'sd7_unit': sd_data.get('sd7_unit')
    }

    return get_or_insert(cursor, 'sd_preparation', data)


def insert_qc_concentrations(cursor, experiment_raw_id: int, qc_data: Dict[str, Any]) -> Optional[int]:
    """
    Insert QC concentration data for an experiment.

    Args:
        cursor: SQLite cursor
        experiment_raw_id: ID of the parent experiment_raw record
        qc_data: Dict containing QC concentration information

    Returns:
        Optional[int]: ID of inserted qc_concentration record, or None if no data
    """
    if not qc_data:
        return None

    data = {
        'experiment_raw_id': experiment_raw_id,
        'qc_l_concentration': qc_data.get('qc_l_concentration'),
        'qc_m_concentration': qc_data.get('qc_m_concentration'),
        'qc_h_concentration': qc_data.get('qc_h_concentration'),
        'qc_unit': qc_data.get('qc_unit')
    }

    return get_or_insert(cursor, 'qc_concentration', data)


def log_experiment_from_form(db_path: str, form_data: Dict[str, Any]) -> int:
    """
    Main function to log a complete experiment from parsed form data.

    Args:
        db_path: Path to SQLite database
        form_data: Complete experiment data from ExpInfoForm

    Returns:
        int: ID of the logged experiment_raw record
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Insert main experiment record
        exp_id = insert_experiment_raw(cursor, form_data)

        # Insert well data if available
        if 'well_data' in form_data:
            well_ids = insert_well_data(cursor, exp_id, form_data['well_data'])

            # Insert readouts if available
            if 'readout_data' in form_data:
                insert_readouts(cursor, well_ids, form_data['readout_data'])

        # Insert SD preparation data if available
        if 'sd_preparation' in form_data:
            insert_sd_preparation(cursor, exp_id, form_data['sd_preparation'])

        # Insert QC concentration data if available
        if 'qc_concentrations' in form_data:
            insert_qc_concentrations(cursor, exp_id, form_data['qc_concentrations'])

        conn.commit()
        print(f"Experiment logged successfully with ID: {exp_id}")
        return exp_id

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()