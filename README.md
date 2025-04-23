# quanti_assay_app

Python-based CLI app for our proteomic quantification assay experiments

## Getting Started

1. Clone the repo:

```bash
git clone https://github.com/wudaudau/quanti_assay_app.git
cd quanti_assay_app
```

2. Create and activate a virtual environment:

This project is developped in Python 3.7.9.

```bash
python3 -m venv venv # I have different versions of Python. python3 is the one I need.
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python main.py
```

## Current Features

- [ ] Main CLI menu with welcome/goodbye flow.

## Roadmap


## Folder Structure

```text
├── data/                   # Store your .sqlite file here
│   └── quanti_assay.sqlite
├── sql/                    # Database schema
│   └── schema.sql
src/
├── app.py                  # Main CLI app
├── database/               # DB logic and loaders
├── assay_lookup/           # Lookup CLI and queries
├── assay_logging/          # Logging CLI and DB interface
├── controllers/            # Interactive flows
tests/                      # Unit tests (coming soon)
```