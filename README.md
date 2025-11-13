# quanti_assay_app

Python-based CLI app for our proteomic quantification assay experiments

## Getting Started

1. Clone the repo:

```bash
git clone https://github.com/wudaudau/quanti_assay_app.git
cd quanti_assay_app
```

2. Create and activate a virtual environment:

This project is developped in Python 3.11.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python main.py
```

## Current Features

1. [Lookup Assay (Full List)](docs/lookup_full_list.md)
2. [Lookup Assay (Step-by-Step Filter)](docs/lookup_step_by_step.md)
3. [Lookup Assay (Filter by Species and Analyte)](docs/lookup_by_analyte.md)
4. [Log Experiment](docs/log_experiment.md)
5. [Lookup Last 15 Experiments](docs/lookup_last_logs.md)
6. [Lookup All Experiments](docs/lookup_all_logs.md)
7. Exit

## Roadmap


## Folder Structure

```text
quanti_assay_app/
├── data/                        # Local SQLite database and data files (not tracked by Git)
│   └── .gitkeep                 # Placeholder to retain folder structure
│   └── quanti_assay.sqlite      # SQLite DB (generated during runtime; ignored by Git)
│
├── doc/                         # 
│   └──                  # 
│
├── src/                         # Source code of the application
│   ├── app.py                   # Main CLI application entry point
│   ├── controllers/             # CLI logic and user interaction flows
│   │   └── main_controller.py   # Main app loop and menu routing
│   │   └── assay_lookup_controller.py   # Step-by-step and name-based assay lookup logic
│   │   └── assay_logging_controller.py  # CLI logic to log experiments
│   │
│   ├── database/                # Database utilities and data loading
│   │   └── db_core.py           # Schema creation and DB initialization
│   │   └── db_utils.py          # Generic helper functions (get_or_insert, etc.)
│   │   └── db_data_loader.py    # Functions to import CSV data into DB
│   │
│   ├── assay_lookup/            # Query logic for assays
│   │   └── assay_lookup.py      # Query helpers (get assay, analytes, etc.)
│   │
│   ├── assay_logging/           # Logic for logging experiment entries
│   │   └── assay_logging.py     # DB interactions to insert and fetch experiment logs
│   ├── data_import/             # Excel file parsing and data extraction
│   │   ├── __init__.py
│   │   ├── exp_reader.py        # Main interface for loading experiment forms
│   │   ├── exp_logger.py        # Database insertion logic for experiments
│   │   ├── assay_to_analyte_map.py # Assay to analyte mapping utilities
│   │   ├── exp_forms/           # Modular experiment form readers
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base ReadExpInfo class and shared utilities
│   │   │   ├── msd_versions/    # MSD-specific form readers by version
│   │   │   │   ├── __init__.py
│   │   │   │   ├── v210305.py   # MSD form reader for version 210305
│   │   │   │   └── ...          # Other MSD version files
│   │   │   └── elisa_versions/  # ELISA-specific form readers by version
│   │   │       ├── __init__.py
│   │   │       ├── v201222.py   # ELISA form reader for version 201222
│   │   │       └── ...          # Other ELISA version files
│   │   └── plate_box_utils/     # Plate layout and data transformation utilities
│   │       └── plate_box_utils.py
│
├── sql/
│   └── schema.sql               # SQL script to initialize the database schema
│
├── tests/                       # Unit and integration tests (future)
│   └── test_app.py              # Tests for CLI and core functions (placeholder)
│
├── .gitignore                   # Ignore database and temporary files
├── main.py                      # 
├── requirements.txt             # Python dependencies (to install with pip)
├── README.md                    # Project documentation
└── TODO.md                      # Development roadmap and task list
```



## Developing commands

- [ ] 8. Add a QC
  - 8 (Add a QC)
  - 1 (Purchased)
  - 1 (Manufacturer A)
  - C4050-1
  - A00C0646
  - QC1 (H)
  - 1 (pg/ml)
  - 2025-01-31
  - y
  - 3
  - 1
  - 100
  - 2
  - 200
  - 3
  - 300
  - y

```bash
cd "/Users/wudaudau/Py projects/GitHub/quanti_assay_app" && rm -f data/quanti_assay.sqlite && echo -e "2\n1\n1\n8\nQC123test\nlot123\nQC-H123\n5\n2025-11-13\nn\n7\n100\ny\nq\nq" | python main.py
```

