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

-- Kit Table (with manufacture and catalog number)
CREATE TABLE IF NOT EXISTS kit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacture_id INTEGER NOT NULL,
    cat_number TEXT NOT NULL,
    format TEXT,   -- New column to store kit format like '1-plate', '5-plate', etc.
    UNIQUE(manufacture_id, cat_number),  -- To avoid duplicates
    FOREIGN KEY (manufacture_id) REFERENCES manufacture(id)
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
    name TEXT NOT NULL,
    qc_type TEXT NOT NULL CHECK (qc_type IN ('Purchased', 'Home made')),
    manufacture_id INTEGER,  -- NULL if home-made
    cat_number TEXT,         -- NULL if home-made
    lot_number TEXT NOT NULL UNIQUE,
    preparation_date TEXT,
    expiration_date TEXT,
    note TEXT,  -- Optional note field
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









-- Assay Lookup View (For assay_lookup)
-- This view summarizes the assay information, including assay_name, species, assay_type, manufacture, kit_cat_number, format
DROP VIEW IF EXISTS assay_lookup_view;

CREATE VIEW assay_lookup_view AS
SELECT 
    a.name AS assay_name, 
    s.name AS species, 
    t.name AS assay_type, 
    m.name AS manufacture, 
    k.cat_number AS kit_cat_number, 
    k.format AS kit_format,
    ana.name AS analyte_name,
    aa.spot_number AS spot_number
FROM assay a
JOIN species s ON a.species_id = s.id
JOIN assay_type t ON a.assay_type_id = t.id
LEFT JOIN assays_kits ak ON a.id = ak.assay_id
LEFT JOIN kit k ON ak.kit_id = k.id
LEFT JOIN manufacture m ON k.manufacture_id = m.id
LEFT JOIN assays_analytes aa ON a.id = aa.assay_id
LEFT JOIN analyte ana ON aa.analyte_id = ana.id
ORDER BY a.name, s.name, t.name, m.name, k.cat_number, k.format, aa.spot_number;

-- QC Lookup View (For qc_lookup)
-- This view summarizes the QC information, including qc_name, qc_type, manufacture, cat_number, lot_number, preparation_date, expiration_date
DROP VIEW IF EXISTS qc_lookup_view;


CREATE VIEW qc_lookup_view AS
SELECT
    qc.lot_number AS lot_number,
    qc.name AS qc_name,  
    a.name AS analyte_name, 
    qa.concentration AS concentration, 
    qa.unit AS unit,
    qc,qc_type AS qc_type,
    m.name AS manufacture_name, 
    qc.cat_number AS cat_number, 
    qc.expiration_date AS expiration_date, 
    qc.preparation_date AS preparation_date
FROM qc
LEFT JOIN manufacture m ON qc.manufacture_id = m.id
LEFT JOIN qc_analyte qa ON qc.id = qa.qc_id
LEFT JOIN analyte a ON qa.analyte_id = a.id