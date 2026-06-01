import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse

API_URL = "https://clashofclans.fandom.com/api.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
}


def _get_page_name(url):
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")
    if path.startswith("wiki/"):
        path = path[len("wiki/"):]
    return unquote(path)


def _fetch_html(url):
    page_name = _get_page_name(url)
    params = {
        "action": "parse",
        "page": page_name,
        "prop": "text",
        "format": "json",
    }

    res = requests.get(API_URL, headers=headers, params=params, timeout=30)
    res.raise_for_status()
    payload = res.json()

    if "error" in payload:
        raise RuntimeError(f"Fandom API error for {url}: {payload['error']}")

    return payload["parse"]["text"]["*"]


def scrape_defense(url):
    # Try fetching with fallback logic
    try:
        html = _fetch_html(url)
    except Exception as exc:
        fallback_url = None
        if url.endswith("/Home_Village"):
            fallback_url = url[:-len("/Home_Village")]
        else:
            fallback_url = url + "/Home_Village"
        
        try:
            html = _fetch_html(fallback_url)
            url = fallback_url
        except Exception:
            raise exc

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="wikitable")

    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue

        # Flatten headers of the first row taking colspan into account
        first_row = rows[0]
        header_cells = first_row.find_all(["th", "td"])
        
        flat_headers = []
        for cell in header_cells:
            colspan = int(cell.get("colspan", 1))
            text = cell.text.strip().lower()
            flat_headers.extend([text] * colspan)

        # We must find "level" and either "cost" or "build cost"
        has_level = any("level" in h for h in flat_headers)
        has_cost = any("cost" in h for h in flat_headers)

        if not (has_level and has_cost):
            continue

        # Map headers to indices
        col_map = {}
        for idx, h in enumerate(flat_headers):
            # Check for level (exclude town hall or builder base details)
            if "level" in h and "town hall" not in h and "required" not in h and "builder" not in h and "laboratory" not in h and "blacksmith" not in h:
                if "level" not in col_map:
                    col_map["level"] = idx
            elif "hitpoints" in h or h == "hp":
                if "hitpoints" not in col_map:
                    col_map["hitpoints"] = idx
            elif "damage per second" in h or h == "dps":
                col_map.setdefault("dps_indices", []).append(idx)
            elif "cost" in h and "boost" not in h and "gear" not in h and "shot" not in h:
                col_map.setdefault("cost_indices", []).append(idx)
            elif "time" in h and "fill" not in h and "gear" not in h:
                if "time" not in col_map or "build" in h or "upgrade" in h or "research" in h:
                    col_map["time"] = idx
            elif "town hall" in h or "th" in h or "required" in h or "laboratory" in h or "blacksmith" in h or "hall" in h or "house" in h:
                # Prioritize Town Hall or TH level required over other details
                if "required_th" not in col_map or "town hall" in h or "th" in h:
                    col_map["required_th"] = idx

        # Set the general list-based properties if we found matching indices
        if "dps_indices" in col_map:
            col_map["dps"] = col_map["dps_indices"]
        if "cost_indices" in col_map:
            col_map["cost"] = col_map["cost_indices"]

        # Validate that we successfully matched core columns (time is optional)
        if "level" not in col_map or "cost" not in col_map:
            continue

        # Detect and skip subheader rows (like Inferno Tower's "Initial" or Hero Equipment's subheaders)
        start_row_idx = 1
        if len(rows) > 1:
            second_row_cells = rows[1].find_all(["th", "td"])
            if all(cell.name == "th" or any(w in cell.text.lower() for w in ["initial", "after", "single", "multi", "duration", "reduction", "ore", "attributes", "boosts"]) for cell in second_row_cells):
                start_row_idx = 2

        levels = {}
        for row in rows[start_row_idx:]:
            cols = [c.text.strip() for c in row.find_all(["td", "th"])]
            
            # Ensure row has enough columns
            time_idx = col_map.get("time")
            required_cols = [
                col_map["level"],
                col_map.get("hitpoints", 0),
                col_map.get("required_th", 0)
            ]
            if time_idx is not None:
                required_cols.append(time_idx)
            if isinstance(col_map.get("dps"), list):
                required_cols.extend(col_map["dps"])
            if isinstance(col_map.get("cost"), list):
                required_cols.extend(col_map["cost"])
            elif isinstance(col_map.get("cost"), int):
                required_cols.append(col_map["cost"])

            if not required_cols or len(cols) <= max(required_cols):
                continue

            level_val = cols[col_map["level"]]
            if not level_val.isdigit():
                continue

            try:
                # 1. Hitpoints
                hp_val = None
                if "hitpoints" in col_map:
                    hp_text = cols[col_map["hitpoints"]].replace(",", "")
                    try:
                        hp_val = int(float(hp_text))
                    except ValueError:
                        if hp_text.isdigit():
                            hp_val = int(hp_text)

                # 2. Damage per Second (DPS)
                dps_val = None
                if "dps" in col_map:
                    if isinstance(col_map["dps"], list):
                        dps_vals = []
                        for idx_dps in col_map["dps"]:
                            if idx_dps < len(cols):
                                text = cols[idx_dps].replace(",", "")
                                # Clean float formatting if present
                                try:
                                    dps_vals.append(str(int(float(text))))
                                except ValueError:
                                    if text:
                                        dps_vals.append(text)
                        dps_val = " / ".join(dps_vals) if dps_vals else None
                    else:
                        dps_text = cols[col_map["dps"]].replace(",", "")
                        try:
                            dps_val = str(int(float(dps_text)))
                        except ValueError:
                            dps_val = dps_text

                # 3. Cost (support list and int)
                cost_val = None
                if "cost" in col_map:
                    if isinstance(col_map["cost"], list):
                        cost_vals = []
                        for idx_c in col_map["cost"]:
                            if idx_c < len(cols):
                                text = cols[idx_c].replace(",", "")
                                if text:
                                    cost_vals.append(text)
                        cost_val = " / ".join(cost_vals) if cost_vals else None
                    else:
                        cost_val = cols[col_map["cost"]]

                # 4. Time
                time_val = cols[time_idx] if time_idx is not None else "Instant"

                # 5. Required progression building level
                th_val = None
                if "required_th" in col_map:
                    th_val = cols[col_map["required_th"]]

                levels[level_val] = {
                    "hitpoints": hp_val,
                    "dps": dps_val,
                    "cost": cost_val,
                    "time": time_val,
                    "required_th": th_val
                }
            except Exception:
                continue

        # Return the first fully matched level stats table
        if levels:
            return levels

    return {}