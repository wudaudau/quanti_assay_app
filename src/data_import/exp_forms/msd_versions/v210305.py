"""
Experiment form for MSD version v20210305.
"""

from ..base import ReadExpInfo
import pandas as pd

class ExpFormMsdV210305(ReadExpInfo):
    assay_type = "MSD"
    form_version = "v20210305"

    @property
    def df_sd7_prep(self):
        sheetname = "SD preparation"
        df = pd.read_excel(self.file, sheet_name=sheetname, header=0, usecols="B:C").dropna(subset=["volume_use_in_sd7"])
        df["total_volume"] = df["volume_use_in_sd7"].sum()
        df["sd7_dilu_factor"] = df["total_volume"] / df["volume_use_in_sd7"]
        df = df.set_index('sd_lot')[['sd7_dilu_factor']].loc[self.sdlots]
        return df

    @property
    def sd_serial_dilu_factor(self):
        return self._ws_sd["D2"].value