import json
import csv
import sys
from pathlib import Path


def convert_json_to_csv(json_path="data/defenses.json", csv_path="data/defenses.csv"):
    """
    Reads a nested Clash of Clans buildings JSON file and flattens it
    into a clean, sorted, tabular CSV file.
    """
    json_path = Path(json_path)
    csv_path = Path(csv_path)

    if not json_path.exists():
        print(f"Error: JSON source file not found at {json_path.resolve()}")
        return False

    print(f"Reading data from {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as exc:
            print(f"Error: Invalid JSON structure in {json_path}: {exc}")
            return False

    # Schema for the output CSV table
    headers = [
        "Category",
        "Building",
        "ID",
        "Level",
        "Hitpoints",
        "DPS",
        "Cost",
        "Time",
        "Required Town Hall",
    ]

    rows = []
    
    # Exclude metadata keys like "last_updated" from categories
    categories = [k for k in data.keys() if k != "last_updated"]

    for category in categories:
        buildings_dict = data[category]
        if not isinstance(buildings_dict, dict):
            continue

        for building_name, building_data in buildings_dict.items():
            building_id = building_data.get("id")
            levels_dict = building_data.get("levels", {})
            if not isinstance(levels_dict, dict):
                continue

            for level, stats in levels_dict.items():
                # Extract columns
                hitpoints = stats.get("hitpoints")
                dps = stats.get("dps")
                cost = stats.get("cost")
                time = stats.get("time")
                required_th = stats.get("required_th")

                rows.append([
                    category.replace("_", " ").title(),  # Clean format e.g. "Builder Base"
                    building_name,
                    building_id if building_id is not None else "",
                    level,
                    hitpoints if hitpoints is not None else "",
                    dps if dps is not None else "",
                    cost if cost is not None else "",
                    time if time is not None else "",
                    required_th if required_th is not None else "",
                ])

    # Sort rows for professional presentation:
    # 1. Category alphabetically
    # 2. Building Name alphabetically
    # 3. Level as ascending integer
    def sort_key(row):
        cat = row[0]
        bld = row[1]
        lvl_str = row[3]
        try:
            lvl = int(lvl_str)
        except ValueError:
            lvl = lvl_str
        return (cat, bld, lvl)

    rows.sort(key=sort_key)

    # Ensure output directory exists and write CSV file
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"Successfully converted {json_path} to CSV at {csv_path}")
        print(f"Total entries written: {len(rows)}")
        return True
    except IOError as exc:
        print(f"Error: Failed to write CSV file at {csv_path}: {exc}")
        return False


if __name__ == "__main__":
    # Allow specifying JSON and CSV paths from command line args
    json_arg = sys.argv[1] if len(sys.argv) > 1 else "data/defenses.json"
    csv_arg = sys.argv[2] if len(sys.argv) > 2 else "data/defenses.csv"
    convert_json_to_csv(json_arg, csv_arg)
