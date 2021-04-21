import json
from pathlib import Path
from typing import Dict


def create_geojson_provinces_with_id(input_f: Path, output_f: Path) -> None:
    """
    Provinces are features of a geojson file and
    each feature is given an id, starts from 1.

    Example:
    ```
    input_geojson:
    {"type": "FeatureCollection",
     "features":[
        {
         "type":"Feature",
         "geometry": {...},
         "properties": {...},
        }
    ]}

    output_geojson:
    {"features":[
        {
         "id": 1,
         "type":"Feature",
         "geometry": {...},
         "properties": {...},
        }
    ]}
    ```
    """

    result = []
    with open(input_f, "rt") as in_f:
        geo_dict = json.load(in_f)
        provinces = geo_dict.get("features")
        for idx, province in enumerate(provinces, start=1):
            province["id"] = idx
            result.append(province)

    with open(output_f, "wt") as out_f:
        json.dump({"features": result}, out_f)


def parse_provinces(input_file: Path) -> Dict[int, str]:
    """
    Given a geojson containing provinces, it returns
    a dictionary of province_id as key, and province_name as value
    e.g {1: "Drenthe", ...}
    """
    id_to_name = {}
    with open(input_file, "rt") as in_f:
        geo_dict = json.load(in_f)
        provinces = geo_dict["features"]
        for province in provinces:
            id, name = province["id"], province["properties"]["name"]
            id_to_name[id] = name
    return id_to_name
