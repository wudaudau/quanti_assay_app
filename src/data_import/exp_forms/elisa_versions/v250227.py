"""
Experiment form for ELISA version v20250227.
"""

from ..base import ReadExpInfo, ASSAY_TO_ANALYTES, plate_to_table_96well
import pandas as pd

class ExpFormElisaV250227(ReadExpInfo):
    assay_type = "ELISA"
    form_version = "v20250227"

    # The form is updated.
        # the version info is on the top of the form
        # Cohort is added
    # The SD preparation is updated to be aligned with the MSD form
    # So I need to update the code to read the new form

    # @property
    # def assay_type(self):
    #     return self._ws_form["A1"].value

    @property
    def expdate(self):
        return str(int(self._ws_form["B6"].value))  # change to datetime object later

    @property
    def project_name(self):
        return self._ws_form["B7"].value

    @property
    def assay_name(self):
        return self._ws_form["B8"].value

    @property
    def sampletype(self):
        return self._ws_form["B9"].value

    @property
    def expinfo(self):
        return self._ws_form["B10"].value  # TODO: Rename to plate_layout_id

    @property
    def manipulator_1(self):
        return self._ws_form["B13"].value

    @property
    def manipulator_2(self):
        return self._ws_form["B14"].value

    @property
    def manipulator_3(self):
        return self._ws_form["B15"].value

    @property
    def manipulators(self):
        expby1 = self._ws_form["B13"].value
        expby2 = self._ws_form["B14"].value
        expby3 = self._ws_form["B15"].value

        expby = [expby1, expby2, expby3]
        # drop empty from the list
        expby = [x for x in expby if x != None]
        expby = [x for x in expby if x != ""]
        return expby

    @property
    def plate_bar_code(self):
        return None

    @property
    def kitcat(self):  # kit cat number
        return self._ws_form["B18"].value

    @property
    def sdcat(self):  # sd cat number
        return self._ws_form["B19"].value

    @property
    def sdlots(self):
        sdlot = self._ws_form["B20"].value

        return [sdlot]  # str(int(x))

    @property
    def qchlot(self):
        return self._ws_form["B22"].value

    @property
    def qcmlot(self):
        return self._ws_form["B23"].value

    @property
    def qcllot(self):
        return self._ws_form["B24"].value

    @property
    def exp_note(self):
        return self._ws_form["B26"].value

    @property
    def exp_form_version(self):
        return self._ws_form["B2"].value

    @property
    def cohort(self):
        return self._ws_form["B28"].value

    @property
    def df_sd7_prep(self):
        """
        only read sd7_prep without the sum
        read the sum values for the calculation
        """
        sheetname = "SD preparation"
        df = pd.read_excel(self.file, sheet_name=sheetname, header=1, usecols="B:C").dropna(subset=["volume (µl)"])
        df = df[df["sd_lot"].isin(self.sdlots)]
        df.rename(columns={"volume (µl)": "volume_use_in_sd7"}, inplace=True)
        df["total_volume"] = self._ws_sd["C9"].value
        df["sd7_dilu_factor"] = df["total_volume"] / df["volume_use_in_sd7"]
        df = df.set_index('sd_lot')[['sd7_dilu_factor']].loc[self.sdlots]
        return df

    @property
    def sd7_dilu_factor(self):
        # TODO: use self df_sd7_prep to obtain it, or we may integrate it with the MSD version.
            # Probably we update the parent class to have the sd7_dilu_factor
        return None

    @property
    def sd_serial_dilu_factor(self):
        # TODO: use self df_sd7_prep to obtain it, or we may integrate it with the MSD version.
            # Probably we update the parent class to have the sd7_dilu_factor
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