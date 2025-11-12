"""
Experiment form for MSD version v20230306.
"""

from ..base import ReadExpInfo
import pandas as pd

class ExpFormMsdV230306(ReadExpInfo):
    # same as v220907
    assay_type = "MSD"
    form_version = "v20230306"

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