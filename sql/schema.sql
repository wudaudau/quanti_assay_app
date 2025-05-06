-- Species Table
CREATE TABLE IF NOT EXISTS species (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Assay Type Table
CREATE TABLE IF NOT EXISTS assay_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Manufacturer Table
CREATE TABLE IF NOT EXISTS manufacturer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Assay Table (basic definition: name, species, type)
CREATE TABLE IF NOT EXISTS assay (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,  -- Your request: enforce unique assay names
    species_id INTEGER NOT NULL,
    assay_type_id INTEGER NOT NULL,
    FOREIGN KEY (species_id) REFERENCES species(id),
    FOREIGN KEY (assay_type_id) REFERENCES assay_type(id)
);

-- Kit Table (with manufacturer and catalog number)
CREATE TABLE IF NOT EXISTS kit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    cat_number TEXT NOT NULL,
    format TEXT,   -- New column to store kit format like '1-plate', '5-plate', etc.
    UNIQUE(manufacturer_id, cat_number),  -- To avoid duplicates
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id)
);

-- Assay-Kit Link Table (associates assays with kits)
CREATE TABLE IF NOT EXISTS assays_kits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assay_id INTEGER NOT NULL,
    kit_id INTEGER NOT NULL,
    FOREIGN KEY (assay_id) REFERENCES assay(id),
    FOREIGN KEY (kit_id) REFERENCES kit(id),
    UNIQUE (assay_id, kit_id)  -- Avoid duplicate links
);

-- Analyte Table (basic list of analytes)
CREATE TABLE IF NOT EXISTS analyte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Assay-Analyte Link Table (associates assays with analytes)
CREATE TABLE IF NOT EXISTS assays_analytes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assay_id INTEGER NOT NULL,
    analyte_id INTEGER NOT NULL,
    spot_number INTEGER NOT NULL,
    FOREIGN KEY (assay_id) REFERENCES assay(id),
    FOREIGN KEY (analyte_id) REFERENCES analyte(id),
    UNIQUE (assay_id, analyte_id)  -- Avoid duplicate links
);




-- QC Table (Quality Control)
CREATE TABLE IF NOT EXISTS qc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lot_number TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    qc_type TEXT NOT NULL CHECK (qc_type IN ('Purchased', 'Home made')),
    manufacturer_id INTEGER,  -- NULL if home-made
    cat_number TEXT,         -- NULL if home-made
    preparation_date TEXT,
    expiration_date TEXT,
    note TEXT,  -- Optional note field
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id)
);

-- QC Analyte Table (links QC to analytes)
CREATE TABLE IF NOT EXISTS qc_analyte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qc_id INTEGER NOT NULL,
    analyte_id INTEGER NOT NULL,
    concentration REAL NOT NULL,
    unit TEXT NOT NULL,
    FOREIGN KEY (qc_id) REFERENCES qc(id),
    FOREIGN KEY (analyte_id) REFERENCES analyte(id),
    UNIQUE (qc_id, analyte_id)  -- Avoid duplicate links
);







-- experiment log

-- Sample Type Table
CREATE TABLE IF NOT EXISTS sample_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Manipulator Table
CREATE TABLE IF NOT EXISTS manipulator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    UNIQUE(first_name, last_name)
);

-- TODO: Experiment Table
-- to have foreign ids for project_name, cohort_name, plate_layout_name, kit_cat_number, sd_cat_number, sd_lot_number, qc_h_lot_number, qc_m_lot_number, qc_l_lot_number to be foreign keys to a project table if needed.
-- CREATE TABLE IF NOT EXISTS experiemnt (
--     FOREIGN KEY (species_id) REFERENCES species(id),
--     FOREIGN KEY (assay_type_id) REFERENCES assay_type(id),
--     FOREIGN KEY (assay_id) REFERENCES assay(id),
--     FOREIGN KEY (sample_type_id) REFERENCES sample_type(id),
--     FOREIGN KEY (manipulator_1_id) REFERENCES manipulator(id),
--     FOREIGN KEY (manipulator_2_id) REFERENCES manipulator(id),
--     FOREIGN KEY (manipulator_3_id) REFERENCES manipulator(id)
-- )


-- Experiment Raw Table (for experiment verbatim data from the ExpInfoForm)
CREATE TABLE IF NOT EXISTS experiment_raw (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exp_date TEXT NOT NULL,
    species TEXT NOT NULL,
    assay_type TEXT NOT NULL,
    assay_name TEXT NOT NULL,
    sample_type TEXT NOT NULL,
    manipulator_1 TEXT NOT NULL,
    manipulator_2 TEXT,
    manipulator_3 TEXT,
    project_name TEXT,
    cohort_name TEXT,
    plate_layout_name TEXT,
    plate_bar_code TEXT,
    kit_cat_number TEXT NOT NULL,
    sd_cat_number TEXT,
    sd_lot_number TEXT,
    qc_h_lot_number TEXT,
    qc_m_lot_number TEXT,
    qc_l_lot_number TEXT,
    notes TEXT
);

-- Table: well_data
-- TODO: Add experiment_id
CREATE TABLE IF NOT EXISTS well_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_raw_id INTEGER NOT NULL,
    well_id TEXT NOT NULL,
    sample_name TEXT,
    sample_role TEXT,
    dilution_factor REAL,
    freeze_thaw_cycle INTEGER,
    excluded BOOLEAN DEFAULT 0,
    FOREIGN KEY (experiment_raw_id) REFERENCES experiment_raw(id),
    UNIQUE (experiment_raw_id, well_id)  -- Avoid duplicate wells in the same experiment
);

-- Table: readout
CREATE TABLE IF NOT EXISTS readout (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    well_data_id INTEGER NOT NULL,
    analyte_name TEXT NOT NULL,
    value REAL,
    unit TEXT,
    readout_type TEXT DEFAULT 'raw',  -- e.g., 'OD', 'MSD intensity'
    FOREIGN KEY (well_data_id) REFERENCES well_data(id)
);

-- Table: sd_preparation
-- TODO: Add experiment_id
CREATE TABLE IF NOT EXISTS sd_preparation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_raw_id INTEGER NOT NULL,
    sd7_concentration REAL,
    serial_dilution_factor REAL,
    sd7_unit TEXT,
    FOREIGN KEY (experiment_raw_id) REFERENCES experiment_raw(id)
);

-- Table: qc_concentration
-- TODO: Add experiment_id
CREATE TABLE IF NOT EXISTS qc_concentration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_raw_id INTEGER NOT NULL,
    qc_l_concentration REAL,
    qc_m_concentration REAL,
    qc_h_concentration REAL,
    qc_unit TEXT,
    FOREIGN KEY (experiment_raw_id) REFERENCES experiment_raw(id)
);

-- Table: file
CREATE TABLE IF NOT EXISTS file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_raw_id INTEGER NOT NULL,
    file_type TEXT,
    file_path TEXT,
    sheet_name TEXT,
    version TEXT,
    FOREIGN KEY (experiment_raw_id) REFERENCES experiment_raw(id)
);

-- Table: result (for processed values)
CREATE TABLE IF NOT EXISTS result (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    well_data_id INTEGER NOT NULL,
    analyte_name TEXT NOT NULL,
    result_value REAL,
    unit TEXT,
    status TEXT,
    FOREIGN KEY (well_data_id) REFERENCES well_data(id)
);







-- Assay Lookup View (For assay_lookup)
-- This view summarizes the assay information, including assay_name, species, assay_type, manufacturer, kit_cat_number, format
DROP VIEW IF EXISTS assay_lookup_view;

CREATE VIEW assay_lookup_view AS
SELECT 
    a.name AS assay_name, 
    s.name AS species, 
    t.name AS assay_type, 
    m.name AS manufacturer, 
    k.cat_number AS kit_cat_number, 
    k.format AS kit_format,
    ana.name AS analyte_name,
    aa.spot_number AS spot_number
FROM assay a
JOIN species s ON a.species_id = s.id
JOIN assay_type t ON a.assay_type_id = t.id
LEFT JOIN assays_kits ak ON a.id = ak.assay_id
LEFT JOIN kit k ON ak.kit_id = k.id
LEFT JOIN manufacturer m ON k.manufacturer_id = m.id
LEFT JOIN assays_analytes aa ON a.id = aa.assay_id
LEFT JOIN analyte ana ON aa.analyte_id = ana.id
ORDER BY a.name, s.name, t.name, m.name, k.cat_number, k.format, aa.spot_number;

-- QC Lookup View (For qc_lookup)
-- This view summarizes the QC information, including qc_name, qc_type, manufacturer, cat_number, lot_number, preparation_date, expiration_date
DROP VIEW IF EXISTS qc_lookup_view;


CREATE VIEW qc_lookup_view AS
SELECT
    qc.lot_number AS lot_number,
    qc.name AS qc_name,  
    a.name AS analyte_name, 
    qa.concentration AS concentration, 
    qa.unit AS unit,
    qc_type AS qc_type,
    m.name AS manufacturer, 
    qc.cat_number AS cat_number, 
    qc.expiration_date AS expiration_date, 
    qc.preparation_date AS preparation_date
FROM qc
LEFT JOIN manufacturer m ON qc.manufacturer_id = m.id
LEFT JOIN qc_analyte qa ON qc.id = qa.qc_id
LEFT JOIN analyte a ON qa.analyte_id = a.id