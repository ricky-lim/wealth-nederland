# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: wealth-nederland
#     language: python
#     name: wealth-nederland
# ---

# %%
# # %load_ext autoreload
# # %autoreload 2

# %%
from pyprojroot import here

from src.app.dashboard import Dashboard
from src.data.geomap import parse_provinces
from src.data.income import Income


# %%
NL_MAP = here() / "data" / "processed" / "nl_provinces_with_id.geojson"
NL_INCOME = here() / "data" / "raw" / "71103ENG.csv"

# %%
nl_provinces = parse_provinces(NL_MAP)
nl_income = Income(input_file=NL_INCOME, province_id_to_name=nl_provinces)
clean_nl_income = nl_income.clean()

# %%
d = Dashboard(df=clean_nl_income, map_file=NL_MAP, province_id_to_name=nl_provinces)
d.build()
