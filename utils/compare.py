from datetime import datetime


def detect_changes(old_levels, new_levels, defense_name):
    changes = []

    for lvl, new_data in new_levels.items():
        old_data = old_levels.get(lvl)

        if not old_data:
            changes.append({
                "type": "NEW_LEVEL",
                "defense": defense_name,
                "level": lvl,
                "data": new_data,
                "time": datetime.now().isoformat()
            })
            continue

        if (old_data.get("cost") != new_data.get("cost") or
            old_data.get("time") != new_data.get("time") or
            old_data.get("required_th") != new_data.get("required_th") or
            old_data.get("hitpoints") != new_data.get("hitpoints") or
            old_data.get("dps") != new_data.get("dps")):
            changes.append({
                "type": "UPDATE",
                "defense": defense_name,
                "level": lvl,
                "old": old_data,
                "new": new_data,
                "time": datetime.now().isoformat()
            })

    return changes