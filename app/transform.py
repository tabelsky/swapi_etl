import re
from typing import Callable

NORMALIZE_FLOAT = re.compile(r",")


def extract_str(data: dict, key: str) -> str:
    return str(data[key])


def extract_id(data: dict, key: str) -> int:
    return int(data[key])


def extract_float(data: dict, key: str) -> float:
    return -1 if data[key] == "unknown" else float(NORMALIZE_FLOAT.sub(".", data[key]))


def extract_films(data: dict, key: str) -> str:
    return ", ".join(item["title"] for item in data[key])


def extract_names(data: dict, key: str) -> str:
    return ", ".join(item["name"] for item in data[key])


def extract_name(data: dict, key: str) -> str:
    return data[key]["name"]


PEOPLE_SCHEMA = {
    "id": extract_id,
    "birth_year": extract_str,
    "eye_color": extract_str,
    "films": extract_films,
    "gender": extract_str,
    "hair_color": extract_str,
    "height": extract_float,
    "homeworld": extract_name,
    "mass": extract_float,
    "skin_color": extract_str,
    "species": extract_names,
    "starships": extract_names,
    "vehicles": extract_names,
}


def transform(raw_data: dict, schema: dict[str, Callable]) -> dict:
    return {key: handler(raw_data, key) for key, handler in schema.items()}


def transform_people(raw_data: dict) -> dict:
    return transform(raw_data, PEOPLE_SCHEMA)
