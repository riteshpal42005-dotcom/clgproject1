import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def extract_csv(filename: str) -> list[dict]:
    """Read a CSV file, ignoring empty lines, and return list of row dictionaries."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with file_path.open("r", newline="", encoding="utf-8-sig") as file:
        lines = [line for line in file if line.strip()]
        return list(csv.DictReader(lines))


def extract_all() -> dict:
    """Extract all raw dataset CSVs."""
    return {
        "products": extract_csv("products.csv"),
        "sales": extract_csv("sales.csv"),
        "sale_items": extract_csv("sale_items.csv"),
    }
