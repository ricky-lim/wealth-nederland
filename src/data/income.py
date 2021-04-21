import cbsodata
import pandas as pd
from pathlib import Path
from typing import Dict


class Income:
    def __init__(self, input_file, province_id_to_name: Dict[int, str]) -> None:
        self.df = pd.read_csv(input_file)
        self.province_id_to_name = province_id_to_name.copy()
        self.province_name_to_id = {v: k for k, v in self.province_id_to_name.items()}
        self.provinces = self.province_name_to_id.keys()

    @staticmethod
    def download(data_id: str, output_file: Path) -> None:
        if Path(output_file).exists():
            return
        df = pd.DataFrame(cbsodata.get_data(data_id))
        df.to_csv(output_file, index=False)

    def filter_by_provinces(self, input_df):
        return input_df[input_df["Region"].isin(self.provinces)]

    def filter_by_household(_, input_df):
        is_household = input_df["Households"] == "Households, total"
        return input_df[is_household]

    def select_columns(_, input_df):
        selected_columns = ["Region", "Period", "MixedIncomeNet_1"]
        input_df["Period"] = input_df["Period"].astype(int)
        return input_df[selected_columns]

    def add_column_province_id(self, input_df):
        # Assign province_id
        province_ids = input_df["Region"].map(self.province_name_to_id)
        return input_df.assign(province_id=province_ids)

    def rename_columns(_, input_df):
        return input_df.rename(
            columns={
                "Region": "province_name",
                "Period": "period",
                "MixedIncomeNet_1": "income",
            }
        )

    def clean(self):
        clean_df = (
            self.df.pipe(self.filter_by_provinces)
            .pipe(self.filter_by_household)
            .pipe(self.select_columns)
            .pipe(self.add_column_province_id)
            .pipe(self.rename_columns)
        )
        return clean_df
