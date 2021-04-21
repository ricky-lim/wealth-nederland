from pyprojroot import here

from src.data.geomap import create_geojson_provinces_with_id, parse_provinces
from src.data.income import Income

DATA_DIR = here() / "data"
INPUT_MAP = DATA_DIR / "raw" / "nl_provinces.geojson"
# ID specified by cbs open data
INCOME_DATA_ID = "71103ENG"
INPUT_INCOME = DATA_DIR / "raw" / f"{INCOME_DATA_ID}.csv"


def main():
    # Prepare provincial map
    # For provincial geojson, each id corresponds to a province
    provincial_map = DATA_DIR / "processed" / "nl_provinces_with_id.geojson"
    create_geojson_provinces_with_id(
        input_f=INPUT_MAP,
        output_f=provincial_map,
    )
    Income.download(data_id=INCOME_DATA_ID, output_file=INPUT_INCOME)


if __name__ == "__main__":
    main()
