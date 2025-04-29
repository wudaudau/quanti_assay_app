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

-- Manufacture Table
CREATE TABLE IF NOT EXISTS manufacture (
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

-- Kit Table (links kit to assays, with manufacture and catalog number)
CREATE TABLE IF NOT EXISTS kit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assay_id INTEGER NOT NULL,
    manufacture_id INTEGER NOT NULL,
    kit_cat_number TEXT NOT NULL,
    format TEXT,   -- New column to store kit format like '1-plate', '5-plate', etc.
    UNIQUE(assay_id, manufacture_id, kit_cat_number),  -- To avoid duplicates
    FOREIGN KEY (assay_id) REFERENCES assay(id),
    FOREIGN KEY (manufacture_id) REFERENCES manufacture(id)
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
    name TEXT NOT NULL,
    qc_type TEXT NOT NULL CHECK (qc_type IN ('Purchased', 'Home made')),
    manufacture_id INTEGER,  -- NULL if home-made
    cat_number TEXT,         -- NULL if home-made
    lot_number TEXT NOT NULL UNIQUE,
    preparation_date TEXT,
    expiration_date TEXT,
    FOREIGN KEY (manufacture_id) REFERENCES manufacture(id)
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
    UNIQUE (qc_id, assay_id)  -- Avoid duplicate links
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

-- Experiment Log Table
CREATE TABLE IF NOT EXISTS exp_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exp_date TEXT NOT NULL,
    species_id INTEGER NOT NULL,
    assay_type_id INTEGER NOT NULL,
    assay_id INTEGER NOT NULL,
    sample_type_id INTEGER NOT NULL,
    manipulator_1_id INTEGER,
    manipulator_2_id INTEGER,
    manipulator_3_id INTEGER,
    FOREIGN KEY (species_id) REFERENCES species(id),
    FOREIGN KEY (assay_type_id) REFERENCES assay_type(id),
    FOREIGN KEY (assay_id) REFERENCES assay(id),
    FOREIGN KEY (sample_type_id) REFERENCES sample_type(id),
    FOREIGN KEY (manipulator_1_id) REFERENCES manipulator(id),
    FOREIGN KEY (manipulator_2_id) REFERENCES manipulator(id),
    FOREIGN KEY (manipulator_3_id) REFERENCES manipulator(id)
);