# TODO - quanti_assay_app

## In Progress

- [ ] "refactor/update-menus"
  - [ ] Draw menu structure
  - [x] Update main_menu_controller.py
  - [ ] Create assay_menu_contoller.py
  - [ ] Update qc_menu_controller.py
  - [ ] Update exp_menu_controller.py

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