"""
Base class for reading experiment information from Excel files.
"""

import pandas as pd
import openpyxl

from src.plate_box_utils.plate_box_utils import plate_to_table_96well  # TODO: I might have published this function somewhere else. Try to include it to my GitHub

from src.data_import.assay_to_analyte_map import ASSAY_TO_ANALYTES


def unique_value_in_df(df):
    v = df.values.reshape([1, -1])[0]  # in a 1d array
    return set(v)


class ReadExpInfo:
    """
    It is a reader to get expinfo from our form.
    The input is the file location.
    """
    assay_type = ""
    form_version = ""

    def __init__(self, file=None):
        if file is not None:
            self.file = file

            # open the file and and the sheets
            wb = openpyxl.load_workbook(file, data_only=True)  # xlrd.open_workbook(filepath)

            sheetname = "form"
            self._ws_form = wb[sheetname]

            sheetname = "SD preparation"
            self._ws_sd = wb[sheetname]

    # @property
    # def assay_type(self):
    #     return self._ws_form["A1"].value

    @property
    def expdate(self):
        return str(int(self._ws_form["B4"].value))  # change to datetime object later

    @property
    def species(self):
        return "Mouse" if self.assay_name == "V-PLEX Proinfammatory P1 Mouse" else "Human"

    @property
    def project_name(self):
        return self._ws_form["B5"].value

    @property
    def cohort(self):  # Cohort name
        return None

    @property
    def assay_name(self):
        return self._ws_form["B6"].value

    @property
    def sampletype(self):
        return self._ws_form["B7"].value

    @property
    def expinfo(self):  # plate layout name, e.g. Soumia202312pl01, igive202312pl01
        return self._ws_form["B8"].value

    @property
    def manipulator_1(self):
        return self._ws_form["B11"].value

    @property
    def manipulator_2(self):
        return self._ws_form["B12"].value

    @property
    def manipulator_3(self):
        return self._ws_form["B13"].value

    @property
    def manipulators(self):  # TODO: We will discard this in the future
        expby1 = self._ws_form["B11"].value
        expby2 = self._ws_form["B12"].value
        expby3 = self._ws_form["B13"].value

        expby = [expby1, expby2, expby3]
        # drop empty from the list
        expby = [x for x in expby if x != None]
        expby = [x for x in expby if x != ""]
        return expby

    @property
    def plate_bar_code(self):
        return self._ws_form["B15"].value

    @property
    def kitcat(self):  # kit cat number
        return None

    @property
    def sdcat(self):  # sd cat number
        return None

    @property
    def sdlots(self):
        sdlot1 = self._ws_form["B17"].value
        sdlot2 = self._ws_form["B18"].value
        sdlot3 = self._ws_form["B19"].value
        sdlot4 = self._ws_form["B20"].value
        sdlot5 = self._ws_form["B21"].value

        sdlots = [sdlot1, sdlot2, sdlot3, sdlot4, sdlot5]
        # drop empty from the list
        sdlots = [x for x in sdlots if x != None]
        sdlots = [x for x in sdlots if x != ""]
        return sdlots  # str(int(x))

    @property
    def qchlot(self):
        return self._ws_form["B23"].value

    @property
    def qcmlot(self):
        return self._ws_form["B24"].value

    @property
    def qcllot(self):
        return self._ws_form["B25"].value

    @property
    def exp_note(self):
        return self._ws_form["B27"].value

    @property
    def exp_form_version(self):
        return self._ws_form["A29"].value

    @property
    def df_sd7_prep(self):
        sheetname = "SD preparation"
        df = pd.read_excel(self.file, sheet_name=sheetname, header=1, usecols="B:D").dropna()
        df = df[df["sd_lot"].isin(self.sdlots)]
        df = df.set_index('sd_lot')[['sd7_dilu_factor']]
        return df

    @property
    def sd7_dilu_factor(self):
        return self.df_sd7_prep['sd7_dilu_factor'].to_dict()

    @property
    def sd_serial_dilu_factor(self):
        return self._ws_sd["H3"].value

    @property
    def df_samplenames(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=1,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8,
                            dtype=str)  # make sure all the dtype of values are str

        return df

    @property
    def df_sampleroles(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=12,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8)

        # check no wrong samplerole anatation in the df
        roles = set(["blank", "standard", "QC", "testing"])
        for i in df.index:
            for c in df.columns:
                v = df.loc[i, c]
                if pd.notnull(v):
                    if v not in roles:
                        raise ValueError("Sample role can only be: {}.".format(", ".join(roles)))

        return df

    @property
    def df_dilutionfactor(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=23,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8)
        # fill 1 if nan
        df.fillna(1, inplace=True)

        return df

    @property
    def df_freezethaw(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=34,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8)
        # fill "unknown" if nan
        df.fillna("unknown", inplace=True)

        return df

    @property
    def df_excluded(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=45,  # the row order, start from 0
                                  index_col=0,  # the col of the selected region -> 0th col
                                  usecols="A:M",
                                  nrows=8)
        # fill False if nan
        df.fillna(False, inplace=True)

        return df

    @property
    def sample_info_df(self):

        def create_df():
            # this df have a col of well_ID of entire 96-well plate
            # and this is the column use to mearge all the data
            df = pd.DataFrame()
            df_index = 1

            for c in list(range(1, 13)):
                for r in ["A", "B", "C", "D", "E", "F", "G", "H", ]:
                    df.loc[df_index, "Well"] = r + "{:02d}".format(c)  # here is different from the ELISA version
                    df_index = df_index + 1
            return df

        def read_and_merge(dataname, input_df, df_to_merge):
            """
            the input_df is in 96-well plate layout
            """

            # creat a temp df to
            temp_df = pd.DataFrame()
            df_index = 1

            # read the data
            for c in input_df.columns:
                for i in input_df.index:
                    temp_df.loc[df_index, "Well"] = i + "{:02d}".format(c)  # here is different from the ELISA version
                    temp_df.loc[df_index, dataname] = input_df.loc[i, c]
                    df_index = df_index + 1

            # mearge the temp_df to the collecting df
            df_merged = pd.merge(df_to_merge, temp_df,
                                        how='outer', on="Well")

            return df_merged

        df_sample_info = create_df()

        df_sample_info = read_and_merge("sample_name", self.df_samplenames, df_sample_info)
        df_sample_info = read_and_merge("sample_role", self.df_sampleroles, df_sample_info)
        df_sample_info = read_and_merge("dilution_factor", self.df_dilutionfactor, df_sample_info)
        df_sample_info = read_and_merge("freeze_thraw_cycle", self.df_freezethaw, df_sample_info)
        df_sample_info = read_and_merge("excluded", self.df_excluded, df_sample_info)

        # excluded set False if na
        df_sample_info["excluded"].fillna(False, inplace=True)
        # The true read from the excle would become 1, replace it to True
        df_sample_info["excluded"].replace(1, True, inplace=True)

        # set dilution_factor to integer
        df_sample_info["dilution_factor"] = df_sample_info["dilution_factor"].astype("int64")

        df_sample_info.set_index("Well", inplace=True)

        # dropna base on sample_name
        df_sample_info.dropna(subset=["sample_name"], inplace=True)

        return df_sample_info