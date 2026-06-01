import zipfile
import io
import lzma
import csv
import json
from pathlib import Path
from datetime import datetime
from utils.file_handler import load_json, save_json, DATA_FILE, CHANGES_FILE
from utils.compare import detect_changes

# Paths config
APKM_PATH = Path("com.supercell.clashofclans_18.367.1-180367002_3arch_7dpi_30lang_1feat_5654015361e6c431e5eadca98d6c4299_apkmirror.com.apkm")
if not APKM_PATH.exists():
    APKM_PATH = Path(r"c:\Users\abc\Desktop\Python\Guess Game\coc-data\com.supercell.clashofclans_18.367.1-180367002_3arch_7dpi_30lang_1feat_5654015361e6c431e5eadca98d6c4299_apkmirror.com.apkm")

RAW_DIR = Path("data/raw_csv")

# Define the targeted logic definition files inside assets/logic/
LOGIC_FILES = {
    "buildings.csv": "buildings.csv",
    "characters.csv": "characters.csv",
    "heroes.csv": "heroes.csv",
    "pets.csv": "pets.csv",
    "traps.csv": "traps.csv",
    "character_items.csv": "character_items.csv"
}

# Supported HV Troops list for filtering
HV_TROOPS = {
    "Barbarian", "Archer", "Giant", "Goblin", "Wall Breaker", "Balloon", "Wizard", "Healer",
    "Dragon", "PEKKA", "Baby Dragon", "Miner", "Electro Dragon", "Yeti", "Dragon Rider",
    "Electro Titan", "Root Rider", "Minion", "Hog Rider", "Valkyrie", "Golem", "Witch",
    "Lava Hound", "Bowler", "Ice Golem", "Headhunter", "Apprentice Warden", "Druid"
}

# Standard core HV Defenses list for filtering
HV_DEFENSES = {
    "Cannon", "Archer Tower", "Mortar", "Air Defense", "Wizard Tower", "Air Sweeper", "Hidden Tesla",
    "Bomb Tower", "X-Bow", "Inferno Tower", "Eagle Artillery", "Scattershot", "Spell Tower", "Monolith"
}


def decompress_sc_csv(raw_data):
    """
    Decompresses a Supercell signed LZMA file.
    - Strips the 68-byte cryptographic signature header.
    - Reconstructs standard 13-byte LZMA stream headers (zero-padding the 4-byte uncompressed size to 8-bytes).
    """
    properties = raw_data[68:69]
    dict_size = raw_data[69:73]
    uncomp_size = raw_data[73:77]
    payload = raw_data[77:]
    
    # Pad 4-byte uncompressed size to standard 8-byte little-endian LZMA spec
    uncomp_size_8 = uncomp_size + b"\x00\x00\x00\x00"
    
    lzma_stream = properties + dict_size + uncomp_size_8 + payload
    return lzma.decompress(lzma_stream).decode("utf-8", errors="ignore")


def make_time_str(d, h, m, s):
    """Formats upgrade days, hours, minutes, and seconds into a clean human string."""
    parts = []
    if d: parts.append(f"{d}d")
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    if s: parts.append(f"{s}s")
    return " ".join(parts) if parts else "Instant"


def parse_raw_csv(csv_content):
    """
    Parses a Supercell logic CSV.
    - Dynamically flattens column headers using the row 0 colspans.
    - Propagates empty entity 'Name' values down from the previous rows.
    - Skips row 1 which contains metadata Types (String, int, boolean).
    """
    reader = csv.reader(io.StringIO(csv_content))
    rows = list(reader)
    if not rows or len(rows) < 3:
        return [], []

    # Reconstruct colspans from row 0
    header_row = rows[0]
    flat_headers = []
    for cell in header_row:
        if cell == "":
            if flat_headers:
                flat_headers.append(flat_headers[-1])
            else:
                flat_headers.append("")
        else:
            flat_headers.append(cell.strip())

    data_rows = []
    current_name = ""
    for r in rows[2:]:
        if not r:
            continue
        if r[0] != "":
            current_name = r[0].strip()
        
        row_dict = {}
        for idx, h in enumerate(flat_headers):
            if h and idx < len(r):
                row_dict[h] = r[idx].strip()
        
        row_dict["Name"] = current_name
        data_rows.append(row_dict)

    return flat_headers, data_rows


def extract_buildings(rows):
    """Parses buildings.csv into defenses, resources, army, and builder_base."""
    categories = {
        "defenses": {},
        "resources": {},
        "army": {},
        "builder_base": {}
    }

    for row in rows:
        name = row.get("Name")
        if not name:
            continue

        is_bb = name.startswith("BB ")
        clean_name = name[3:] if is_bb else name

        if is_bb:
            target_cat = "builder_base"
        elif clean_name in HV_DEFENSES or row.get("BuildingClass") == "Defense":
            target_cat = "defenses"
        elif row.get("BuildingClass") == "Resource":
            target_cat = "resources"
        elif row.get("BuildingClass") in ["Army", "Laboratory", "Barracks", "Spell Factory", "Blacksmith", "Workshop", "Pet"] or clean_name in ["Blacksmith", "Pet House", "Siege Workshop", "Barracks", "Dark Barracks"]:
            target_cat = "army"
        else:
            continue

        lvl = row.get("BuildingLevel", row.get("Level", "1"))
        if not lvl.isdigit():
            continue

        d = int(row.get("BuildTimeD", 0)) if row.get("BuildTimeD") else 0
        h = int(row.get("BuildTimeH", 0)) if row.get("BuildTimeH") else 0
        m = int(row.get("BuildTimeM", 0)) if row.get("BuildTimeM") else 0
        s = int(row.get("BuildTimeS", 0)) if row.get("BuildTimeS") else 0
        time_str = make_time_str(d, h, m, s)

        cost = row.get("BuildCost", "0")
        if cost == "0" or not cost:
            cost = "N/A"
            if time_str == "Instant":
                time_str = "N/A"

        hp = row.get("Hitpoints")
        hp_val = int(hp) if hp and hp.isdigit() else None

        dps = row.get("DPS")
        dps_val = str(int(dps)) if dps and dps.isdigit() else None

        required_th = row.get("TownHallLevel", "1")

        categories[target_cat].setdefault(clean_name, {"levels": {}})[ "levels"][lvl] = {
            "hitpoints": hp_val,
            "dps": dps_val,
            "cost": cost,
            "time": time_str,
            "required_th": required_th
        }

    return categories


def extract_characters(rows):
    """Parses characters.csv into troops and builder_base_troops."""
    categories = {
        "troops": {},
        "builder_base_troops": {}
    }

    for row in rows:
        name = row.get("Name")
        if not name:
            continue

        is_bb = name.startswith("BB ")
        clean_name = name[3:] if is_bb else name

        if is_bb:
            target_cat = "builder_base_troops"
        elif clean_name in HV_TROOPS:
            target_cat = "troops"
        else:
            continue

        lvl = row.get("UpgradeLevel", row.get("Level", "1"))
        if not lvl.isdigit():
            try:
                lvl = str(int(row.get("UpgradeLevel", 0)) + 1)
            except ValueError:
                continue

        d = int(row.get("UpgradeTimeD", 0)) if row.get("UpgradeTimeD") else 0
        h = int(row.get("UpgradeTimeH", 0)) if row.get("UpgradeTimeH") else 0
        m = int(row.get("UpgradeTimeM", 0)) if row.get("UpgradeTimeM") else 0
        s = int(row.get("UpgradeTimeS", 0)) if row.get("UpgradeTimeS") else 0
        time_str = make_time_str(d, h, m, s)

        cost = row.get("UpgradeCost", "0")
        if cost == "0" or not cost:
            cost = "N/A"
            if time_str == "Instant":
                time_str = "N/A"

        hp = row.get("Hitpoints")
        hp_val = int(hp) if hp and hp.isdigit() else None

        dps = row.get("DPS")
        dps_val = str(int(dps)) if dps and dps.isdigit() else None

        required_th = row.get("LaboratoryLevelRequired", row.get("StarLaboratoryLevelRequired", "1"))
        if not required_th or required_th == "0":
            required_th = "N/A"

        categories[target_cat].setdefault(clean_name, {"levels": {}})[ "levels"][lvl] = {
            "hitpoints": hp_val,
            "dps": dps_val,
            "cost": cost,
            "time": time_str,
            "required_th": required_th
        }

    return categories


def extract_heroes(rows):
    """Parses heroes.csv into heroes."""
    category = {}

    for row in rows:
        name = row.get("Name")
        if not name:
            continue

        is_bb = name.startswith("BB ")
        clean_name = name[3:] if is_bb else name

        if clean_name not in ["Barbarian King", "Archer Queen", "Grand Warden", "Royal Champion", "Battle Machine", "Battle Copter"]:
            continue

        lvl = row.get("Level", "1")
        if not lvl.isdigit():
            continue

        d = int(row.get("UpgradeTimeD", 0)) if row.get("UpgradeTimeD") else 0
        h = int(row.get("UpgradeTimeH", 0)) if row.get("UpgradeTimeH") else 0
        m = int(row.get("UpgradeTimeM", 0)) if row.get("UpgradeTimeM") else 0
        s = int(row.get("UpgradeTimeS", 0)) if row.get("UpgradeTimeS") else 0
        time_str = make_time_str(d, h, m, s)

        cost = row.get("UpgradeCost", "0")
        if cost == "0" or not cost:
            cost = "N/A"
            if time_str == "Instant":
                time_str = "N/A"

        hp = row.get("Hitpoints")
        hp_val = int(hp) if hp and hp.isdigit() else None

        dps = row.get("DPS")
        dps_val = str(int(dps)) if dps and dps.isdigit() else None

        required_th = row.get("TownHallLevelRequired", "1")

        category.setdefault(clean_name, {"levels": {}})[ "levels"][lvl] = {
            "hitpoints": hp_val,
            "dps": dps_val,
            "cost": cost,
            "time": time_str,
            "required_th": required_th
        }

    return {"heroes": category}


def extract_pets(rows):
    """Parses pets.csv into pets."""
    category = {}

    for row in rows:
        name = row.get("Name")
        if not name:
            continue

        clean_name = "L.A.S.S.I" if name == "LASSI" else name

        if clean_name not in ["L.A.S.S.I", "Mighty Yak", "Electro Owl", "Unicorn", "Phoenix", "Poison Lizard", "Diggy", "Frosty", "Spirit Fox", "Angry Jelly"]:
            continue

        try:
            lvl = str(int(row.get("UpgradeLevel", 0)) + 1)
        except ValueError:
            continue

        d = int(row.get("UpgradeTimeD", 0)) if row.get("UpgradeTimeD") else 0
        h = int(row.get("UpgradeTimeH", 0)) if row.get("UpgradeTimeH") else 0
        m = int(row.get("UpgradeTimeM", 0)) if row.get("UpgradeTimeM") else 0
        s = int(row.get("UpgradeTimeS", 0)) if row.get("UpgradeTimeS") else 0
        time_str = make_time_str(d, h, m, s)

        cost = row.get("UpgradeCost", "0")
        if cost == "0" or not cost:
            cost = "N/A"
            if time_str == "Instant":
                time_str = "N/A"

        hp = row.get("Hitpoints")
        hp_val = int(hp) if hp and hp.isdigit() else None

        dps = row.get("DPS")
        dps_val = str(int(dps)) if dps and dps.isdigit() else None

        required_th = row.get("PetHouseLevelRequired", "1")

        category.setdefault(clean_name, {"levels": {}})[ "levels"][lvl] = {
            "hitpoints": hp_val,
            "dps": dps_val,
            "cost": cost,
            "time": time_str,
            "required_th": required_th
        }

    return {"pets": category}


def extract_traps(rows):
    """Parses traps.csv into traps and builder_base_traps."""
    categories = {
        "traps": {},
        "builder_base_traps": {}
    }

    for row in rows:
        name = row.get("Name")
        if not name:
            continue

        is_bb = name.startswith("BB ")
        clean_name = name[3:] if is_bb else name

        if is_bb:
            target_cat = "builder_base_traps"
        elif clean_name in ["Bomb", "Spring Trap", "Air Bomb", "Giant Bomb", "Seeking Air Mine", "Skeleton Trap", "Tornado Trap"]:
            target_cat = "traps"
        else:
            continue

        lvl = row.get("Level", "1")
        if not lvl.isdigit():
            continue

        d = int(row.get("BuildTimeD", 0)) if row.get("BuildTimeD") else 0
        h = int(row.get("BuildTimeH", 0)) if row.get("BuildTimeH") else 0
        m = int(row.get("BuildTimeM", 0)) if row.get("BuildTimeM") else 0
        s = int(row.get("BuildTimeS", 0)) if row.get("BuildTimeS") else 0
        time_str = make_time_str(d, h, m, s)

        cost = row.get("BuildCost", "0")
        if cost == "0" or not cost:
            cost = "N/A"
            if time_str == "Instant":
                time_str = "N/A"

        required_th = row.get("TownHallLevel", "1")

        categories[target_cat].setdefault(clean_name, {"levels": {}})[ "levels"][lvl] = {
            "hitpoints": None,
            "dps": None,
            "cost": cost,
            "time": time_str,
            "required_th": required_th
        }

    return categories


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not APKM_PATH.exists():
        print(f"Error: APKM archive not found at {APKM_PATH}")
        return

    print(f"Unpacking asset pack from {APKM_PATH}...")
    decompressed_data = {}

    with zipfile.ZipFile(APKM_PATH, "r") as z:
        apk_data = z.read("split_install_time_asset_pack.apk")
        with zipfile.ZipFile(io.BytesIO(apk_data), "r") as apk:
            for file_name in LOGIC_FILES.keys():
                print(f"Extracting and decompressing logic/{file_name}...")
                raw_bytes = apk.read(f"assets/logic/{file_name}")
                
                # Save raw compressed files as backup in data/raw_csv
                (RAW_DIR / f"{file_name}.sc").write_bytes(raw_bytes)
                
                # Decompress
                csv_content = decompress_sc_csv(raw_bytes)
                
                # Save decompressed raw CSV
                (RAW_DIR / file_name).write_text(csv_content, encoding="utf-8")
                decompressed_data[file_name] = csv_content

    # Now parse decompressed data
    master_data = {}
    
    # 1. Parse Buildings
    print("Parsing buildings...")
    _, buildings_rows = parse_raw_csv(decompressed_data["buildings.csv"])
    b_cats = extract_buildings(buildings_rows)
    master_data.update(b_cats)

    # 2. Parse Characters (Troops & BB Troops)
    print("Parsing characters...")
    _, char_rows = parse_raw_csv(decompressed_data["characters.csv"])
    c_cats = extract_characters(char_rows)
    master_data.update(c_cats)

    # 3. Parse Heroes
    print("Parsing heroes...")
    _, hero_rows = parse_raw_csv(decompressed_data["heroes.csv"])
    h_cats = extract_heroes(hero_rows)
    master_data.update(h_cats)

    # 4. Parse Pets
    print("Parsing pets...")
    _, pet_rows = parse_raw_csv(decompressed_data["pets.csv"])
    p_cats = extract_pets(pet_rows)
    master_data.update(p_cats)

    # 5. Parse Traps (HV & BB traps)
    print("Parsing traps...")
    _, trap_rows = parse_raw_csv(decompressed_data["traps.csv"])
    t_cats = extract_traps(trap_rows)
    master_data.update(t_cats)

    # 6. Parse Hero Equipment (character_items.csv)
    print("Parsing hero equipment...")
    reader = csv.reader(io.StringIO(decompressed_data["character_items.csv"]))
    ci_rows = list(reader)
    
    equipment_cat = {}
    if len(ci_rows) > 2:
        current_name = ""
        for r in ci_rows[2:]:
            if not r:
                continue
            if r[0] != "":
                current_name = r[0].strip()
                
            if current_name not in ["Barbarian Puppet", "Rage Vial", "Archer Puppet", "Invisibility Vial", "Eternal Tome", "Life Gem", "Giant Gauntlet", "Earthquake Boots", "Healer Puppet", "Rage Gem", "Healing Tome"]:
                continue
                
            lvl = r[1].strip()
            if not lvl.isdigit():
                continue
                
            res_list = [x.strip() for x in r[13].split(";")] if len(r) > 13 and r[13] else []
            cost_list = [x.strip() for x in r[14].split(";")] if len(r) > 14 and r[14] else []

            shiny = "-"
            glowy = "-"
            starry = "-"

            for res, cost in zip(res_list, cost_list):
                if not res or not cost:
                    continue
                if res == "CommonOre":
                    shiny = cost
                elif res == "RareOre":
                    glowy = cost
                elif res == "EpicOre":
                    starry = cost

            if shiny == "-" and glowy == "-" and starry == "-":
                cost_str = "N/A"
            else:
                cost_str = f"{shiny} / {glowy} / {starry}"

            hp_val = None
            if len(r) > 20 and r[20].strip():
                try:
                    hp_val = int(float(r[20].strip()))
                except ValueError:
                    hp_val = None

            dps_val = None
            if len(r) > 23 and r[23].strip():
                try:
                    dps_val = str(int(float(r[23].strip())))
                except ValueError:
                    dps_val = None

            required_blacksmith = r[11].strip() if len(r) > 11 else "1"

            equipment_cat.setdefault(current_name, {"levels": {}})[ "levels"][lvl] = {
                "hitpoints": hp_val,
                "dps": dps_val,
                "cost": cost_str,
                "time": "Instant",
                "required_th": required_blacksmith
            }
            
    master_data["hero_equipment"] = equipment_cat

    # Clean names for Builder Base Category
    for cat in ["builder_base_troops", "builder_base_traps"]:
        if cat in master_data:
            cleaned = {}
            for name, val in master_data[cat].items():
                clean_name = name
                if name.startswith("BB "):
                    clean_name = name[3:]
                if clean_name == "Power PEKKA":
                     clean_name = "Power P.E.K.K.A"
                cleaned[clean_name] = val
            master_data[cat] = cleaned

    master_data["last_updated"] = datetime.now().isoformat()

    # Change detection
    data = load_json(DATA_FILE)
    changes_log = load_json(CHANGES_FILE)
    all_changes = []

    categories_keys = [k for k in master_data.keys() if k != "last_updated"]
    for category in categories_keys:
        if category not in data:
            data[category] = {}

        for item_name, item_val in master_data[category].items():
            new_levels = item_val.get("levels", {})
            old_levels = data[category].get(item_name, {}).get("levels", {})
            changes = detect_changes(old_levels, new_levels, item_name)

            if changes:
                print(f"{len(changes)} changes found in {item_name} ({category})")
                all_changes.extend(changes)

            data[category][item_name] = item_val

    data["last_updated"] = master_data["last_updated"]
    save_json(DATA_FILE, data)

    if all_changes:
        changes_log.setdefault("history", []).extend(all_changes)
        save_json(CHANGES_FILE, changes_log)

    # Generate and save clean flat CSV spreadsheet
    csv_path = Path("data/defenses.csv")
    headers = ["Category", "Building", "Level", "Hitpoints", "DPS", "Cost", "Time", "Required Town Hall"]
    
    rows_to_write = []
    for category in categories_keys:
        buildings_dict = master_data[category]
        for building_name, building_data in buildings_dict.items():
            levels_dict = building_data.get("levels", {})
            for level, stats in levels_dict.items():
                rows_to_write.append([
                    category.replace("_", " ").title(),
                    building_name,
                    level,
                    stats.get("hitpoints") if stats.get("hitpoints") is not None else "",
                    stats.get("dps") if stats.get("dps") is not None else "",
                    stats.get("cost") if stats.get("cost") is not None else "",
                    stats.get("time") if stats.get("time") is not None else "",
                    stats.get("required_th") if stats.get("required_th") is not None else ""
                ])

    def sort_key(row):
        cat = row[0]
        bld = row[1]
        lvl_str = row[2]
        try:
            lvl = int(lvl_str)
        except ValueError:
            lvl = lvl_str
        return (cat, bld, lvl)

    rows_to_write.sort(key=sort_key)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows_to_write)
        
    print(f"Processed CSV database successfully saved at {csv_path}")
    print("Update completed.")


if __name__ == "__main__":
    main()