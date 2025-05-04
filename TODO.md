# TODO - quanti_assay_app

## In Progress

- [ ] "refactor/qc-menu-funcs" from "refactor/update-menus"
  - [x] Create "refactor/qc-menu-funcs" branch
  - [ ] Develop qc lookup functions
    - [ ] Make a qc_loopup_menu
    - [ ] Refactor Add a QC function
    - [x] Import QC data
- [ ] "refactor/update-menus"
  - [ ] Draw menu structure
    - Main menu
      - Sub menus (e.g. Assay Menu) (Use "menu" in the names)
        - Functional flows (e.g. xxx_lookup_flow, xxx_log_flow)
          - Asking opitons
  - [x] Update `main_menu_controller.py` and make it work
  - [x] Create `assay_menu_contoller.py` and make it work
  - [x] Create `qc_menu_controller.py` and make it work
  - [x] Create `exp_menu_controller.py` and make it work
  - [x] Create `show_flow_title_and_descriptions()` in messages_and_ask_questions.py and applys to flows.
  - [ ] Enhance the flow functionality using "1. Assay Menu -> 3. Lookup Assay (Filter by Species and Analyte)".
  - [x] Rename `messages_and_ask_questions.py` to `controller_utils.py`
  - [ ] What to do next? Develop the submenu and ensure the functionality? Add data to the database? More complex function such as asking password to access the log function?
- [x] "refactor/db-schema-kit-assay"
  - [x] Refactor database schema
  - [ ] Refactor related python functions
    - [x] Add a table update function in `db_utils.py`
    - [ ] assay_analyte -> assays_analyte table related
    - [ ] Any code that used `kit.assay_id`
    - [ ] Any queries, data creation, and form submissions

- [ ] Refactor the app into `feature/refactor-app` branch.
  - [ ] Add function-related documentations.
  - [ ] Keep real data (e.g. Manipulators) in our place -> Add instruction to prepare the inital database.
    - [ ] Sensitive data:
      - [ ] Manipulators
      - [ ] Expriment log.
  - [ ] What are the pre-set tables in the database and how to prepare the data in csv files?
  - [ ] There are two main functions: 1) Lookup and 2) Log Exp. Refactor them by working flow. E.g. Before assay (purchase the reagent, prepare the sample, download the protocol ...), After assay ...

## Next Up

- [ ] Remove "Manipulators" data from the repo.
- [ ] Add tools or modules to ensre the app can run correctly. E.g. set different combination of input as scenarios.
- [ ] Create the unittests.

## Wishlist

- Functions to show the most used kit from the exp log.

## Done

- [x] Move main CLI app into `feature/main-cli-app` branch.
  - [x] Move `main.py`, `src/app.py`, and related elements (py modules, db schema in sql, data in csv to initiate the database, etc).
  - [x] Add function discriptions in `README.md`.
- [x] Create unittest into `text/db_utils` branch.
- [x] "refactor/assay-lookup-func"
  - [x] Create a VIEW for assay_lookup
  - [x] Use `assay_lookup_view` in `assay_lookup.py`
    - [x] Update assay_lookup_view schema to have analyte and spot
    - [x] Use updated view in `assay_loopup.py`
  - [x] Refactor the lookup flows to make them easy to understad and use.
    - [x] `assay_lookup_flow_no_filter()`
    - [x] `assay_lookup_flow_filter_by_species_and_assay_type`
    - [x] `assay_lookup_flow_filter_by_species_and_analyte`
