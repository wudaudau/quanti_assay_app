




"""
Here are functions:
    - iter_well
"""

import pandas as pd

def iter_well(format="96-well plate", iter_by="row"):
    """
    To get the well_id in order either by row or by column.
    We can also choose different plate or boxes.

    format: "96-well plate", "9x9 box", "10x10 box"
    iter_by: "row" or "col"
    """

    def iter_by_r(rows, cols):
        ls = []
        for r in rows:
            for c in cols:
                ls.append(r + "{:02d}".format(c))
        return ls

    def iter_by_c(rows, cols):
        ls = []
        for c in cols:
            for r in rows:
                ls.append(r + "{:02d}".format(c))
        return ls

    if format == "96-well plate":
        rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
        cols = list(range(1,13))
        if iter_by == "row":
            return iter_by_r(rows, cols)
        elif iter_by == "col":
            return iter_by_c(rows, cols)

    elif format == "9x9 box":
        rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        cols = list(range(1,10))
        if iter_by == "row":
            return iter_by_r(rows, cols)
        elif iter_by == "col":
            return iter_by_c(rows, cols)

    elif format == "10x10 box":
        rows = list(range(1,11))
        cols = list(range(0,10))
        if iter_by == "row":
            return list(range(1,101))
        elif iter_by == "col":
            ls = [1,11,21,31,41,51,61,71,81,91,
                2,12,22,32,42,52,62,72,82,92,
                3,13,23,33,43,53,63,73,83,93,
                4,14,24,34,44,54,64,74,84,94,
                5,15,25,35,45,55,65,75,85,95,
                6,16,26,36,46,56,66,76,86,96,
                7,17,27,37,47,57,67,77,87,97,
                8,18,28,38,48,58,68,78,88,98,
                9,19,29,39,49,59,69,79,89,99,
                10,20,30,40,50,60,70,80,90,100]
            return ls

    else:
        return "Wrong format."

# iter_well("10x10 box", iter_by="col")






def create_96_well_plate_df():
    """
    This is to generate a blank DataFrame to 
    """
    r = ["A","B","C","D","E","F","G","H"]
    c = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    return pd.DataFrame(index=r, columns=c)

def create_96_well_table_df():
    # this df have a col of well_ID of entire 96-well plate
    # and this is the column use to mearge all the data
    # set the well in index

    df = pd.DataFrame(index=iter_well("96-well plate"))
    df.index.name = "Well"

    return df
    

def plate_to_table_96well(df_plate, var_name):
    """
    To get the value from the plate and put in a output df.
    The output df will with well_id in the index
    dorpna
    we ignore the index order at this step.
    """
    df_table = pd.DataFrame(columns=[var_name])
    df_table.index.name = "Well"

    for r in df_plate.index:
        for c in df_plate.columns:
            w = "{}{:02d}".format(r, c) # the c is int
            # w = "{}{}".format(r, c) # the c in already a 2-digit string
            v = df_plate.loc[r, c]

            df_table.loc[w, var_name] = v

    return df_table.dropna()

# def table_to_plate_96well(df_table, col_name_for_well, col_name_for_value):
#     """
#     no duplicates for well_id!
#     well_id is like A01......

#     col_name_for_well can be index???
#     """
#     # new a plate to store values from table
#     df_plate = create_96_well_plate_df()

#     # reset index 
#     df_table = df_table.reset_index()

#     # transform well to r_id and c_id
#     df_table["r_id"] = df_table[col_name_for_well].str.slice(0, 1)
#     df_table["c_id"] = df_table[col_name_for_well].str.slice(1, 3)

#     for i in df_table.index:
#         r_id = df_table.loc[i, "r_id"]
#         c_id = df_table.loc[i, "c_id"]
#         v = df_table.loc[i, col_name_for_value]

#         df_plate.loc[r_id, c_id] = v

#     return df_plate

def table_to_plate_96well(df_table):
    """
    the input df is with 
        well_id in the index and value
        one single colume with the value

    no duplicates for well_id!
    well_id is like A01......
    """
    # check no duplicated well
    if True not in df_table.index.duplicated():

        # new a plate to store values from table
        df_plate = create_96_well_plate_df()

        col = df_table.columns[0]

        for w in df_table.index:
            r_id = w[0]
            c_id = w[1:3]
            v = df_table.loc[w, col]

            df_plate.loc[r_id, c_id] = v

        return df_plate




"""
Above this, there are things written in the original "quanti_data_process"
"""


