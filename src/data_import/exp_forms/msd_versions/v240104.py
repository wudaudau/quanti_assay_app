"""
Experiment form for MSD version v20240104.
"""

from ..base import ReadExpInfo
import pandas as pd

class ExpFormMsdV240104(ReadExpInfo):
    # same as v220907
    assay_type = "MSD"
    form_version = "v20240104"

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
    def expinfo(self):  # plate layout id, e.g. Soumia202312pl01, igive202312pl01
        return self._ws_form["B10"].value

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
        return self._ws_form["B17"].value

    @property
    def sdlots(self):
        sdlot1 = self._ws_form["B19"].value
        sdlot2 = self._ws_form["B20"].value
        sdlot3 = self._ws_form["B21"].value
        sdlot4 = self._ws_form["B22"].value
        sdlot5 = self._ws_form["B23"].value

        sdlots = [sdlot1, sdlot2, sdlot3, sdlot4, sdlot5]
        # drop empty from the list
        sdlots = [x for x in sdlots if x != None]
        sdlots = [x for x in sdlots if x != ""]
        return sdlots  # str(int(x))

    @property
    def qchlot(self):
        return self._ws_form["B25"].value

    @property
    def qcmlot(self):
        return self._ws_form["B26"].value

    @property
    def qcllot(self):
        return self._ws_form["B27"].value

    @property
    def exp_note(self):
        return self._ws_form["B29"].value

    @property
    def exp_form_version(self):
        return self._ws_form["B2"].value

    @property
    def cohort(self):
        return self._ws_form["B31"].value

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