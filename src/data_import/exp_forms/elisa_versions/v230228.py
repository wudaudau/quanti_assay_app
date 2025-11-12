"""
Experiment form for ELISA version v20230228.
"""

from ..base import ReadExpInfo, ASSAY_TO_ANALYTES, plate_to_table_96well
import pandas as pd

class ExpFormElisaV230228(ReadExpInfo):
    # the same as ExpFormElisaV210310 except the form version
    assay_type = "ELISA"
    form_version = "v20230228"

    @property
    def plate_bar_code(self):
        return None

    @property
    def kitcat(self):  # kit cat number
        return self._ws_form["B16"].value

    @property
    def sdcat(self):  # sd cat number
        return self._ws_form["B17"].value

    @property
    def sdlots(self):
        sdlot = self._ws_form["B18"].value

        return [sdlot]  # str(int(x))

    @property
    def qchlot(self):
        return self._ws_form["B20"].value

    @property
    def qcmlot(self):
        return self._ws_form["B21"].value

    @property
    def qcllot(self):
        return self._ws_form["B22"].value

    @property
    def exp_note(self):
        return self._ws_form["B24"].value

    @property
    def exp_form_version(self):
        return self._ws_form["A25"].value

    @property
    def sd7_dilu_factor(self):
        return None

    @property
    def sd_serial_dilu_factor(self):
        return None

    @property
    def df_450_570nm(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=1,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8)
        return df

    @property
    def df_450nm(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=12,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8)
        return df

    @property
    def df_570nm(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=23,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8)
        return df

    @property
    def df_samplenames(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=34,  # the row order, start from 0
                            index_col=0,  # the col of the selected region -> 0th col
                            usecols="A:M",
                            nrows=8)
        return df

    @property
    def df_sampleroles(self):
        sheetname = "sample info"

        df = pd.read_excel(self.file, sheetname, engine="openpyxl",
                          header=45,  # the row order, start from 0
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
                          header=56,  # the row order, start from 0
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
                          header=67,  # the row order, start from 0
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
                          header=78,  # the row order, start from 0
                                  index_col=0,  # the col of the selected region -> 0th col
                                  usecols="A:M",
                                  nrows=8)
        # fill False if nan
        df.fillna(False, inplace=True)

        return df

    @property
    def readout_df(self):
        # make it as readout_df
            # It's a long table
            # columns: Well, analyte, value, reaout_type
            # readout_type: 'OD 450-570 nm', 'OD 450 nm', 'OD 570 nm', 'MSD ECL intensity', 'Luminex MFI'

        # obtain the analyte_name based on the assay_name
        analyte = ASSAY_TO_ANALYTES[self.assay_name]

        df_opt = pd.DataFrame(columns=["Well", "Analyte", "value", "readout_type"])

        # obtain the readout to df_opt
        for value_in_layout_df, readout_type in ((self.df_450_570nm, "OD 450-570 nm"),
                                                 (self.df_450nm, "OD 450 nm"),
                                                 (self.df_570nm, "OD 570 nm")):

            df_temp = plate_to_table_96well(value_in_layout_df, "value")  # the index name is Well

            # make sure the column is numeric
            df_temp["value"] = df_temp["value"].astype("float64")

            # add readout_type and analyte to the df_temp
            df_temp["readout_type"] = readout_type
            df_temp["Analyte"] = analyte

            # reset the index
            df_temp.reset_index(inplace=True)

            # concatenate the df_temp to the df_opt
            df_opt = pd.concat([df_opt, df_temp], ignore_index=True, axis=0)

        return df_opt