from datetime import datetime
from utils.file_handler import load_json, save_json, DATA_FILE, CHANGES_FILE
from utils.compare import detect_changes
from scrapers.update_defenses import scrape_defense

# All Clash of Clans categories and structures to crawl (115+ items)
CATEGORIES = {
    "defenses": {
        "Cannon": "https://clashofclans.fandom.com/wiki/Cannon/Home_Village",
        "Archer Tower": "https://clashofclans.fandom.com/wiki/Archer_Tower/Home_Village",
        "Mortar": "https://clashofclans.fandom.com/wiki/Mortar/Home_Village",
        "Air Defense": "https://clashofclans.fandom.com/wiki/Air_Defense/Home_Village",
        "Wizard Tower": "https://clashofclans.fandom.com/wiki/Wizard_Tower/Home_Village",
        "Air Sweeper": "https://clashofclans.fandom.com/wiki/Air_Sweeper/Home_Village",
        "Hidden Tesla": "https://clashofclans.fandom.com/wiki/Hidden_Tesla/Home_Village",
        "Bomb Tower": "https://clashofclans.fandom.com/wiki/Bomb_Tower/Home_Village",
        "X-Bow": "https://clashofclans.fandom.com/wiki/X-Bow/Home_Village",
        "Inferno Tower": "https://clashofclans.fandom.com/wiki/Inferno_Tower/Home_Village",
        "Eagle Artillery": "https://clashofclans.fandom.com/wiki/Eagle_Artillery/Home_Village",
        "Scattershot": "https://clashofclans.fandom.com/wiki/Scattershot/Home_Village",
        "Spell Tower": "https://clashofclans.fandom.com/wiki/Spell_Tower/Home_Village",
        "Monolith": "https://clashofclans.fandom.com/wiki/Monolith/Home_Village"
    },
    "resources": {
        "Gold Mine": "https://clashofclans.fandom.com/wiki/Gold_Mine/Home_Village",
        "Elixir Collector": "https://clashofclans.fandom.com/wiki/Elixir_Collector/Home_Village",
        "Dark Elixir Drill": "https://clashofclans.fandom.com/wiki/Dark_Elixir_Drill/Home_Village",
        "Gold Storage": "https://clashofclans.fandom.com/wiki/Gold_Storage/Home_Village",
        "Elixir Storage": "https://clashofclans.fandom.com/wiki/Elixir_Storage/Home_Village",
        "Dark Elixir Storage": "https://clashofclans.fandom.com/wiki/Dark_Elixir_Storage/Home_Village",
        "Clan Castle": "https://clashofclans.fandom.com/wiki/Clan_Castle/Home_Village"
    },
    "army": {
        "Army Camp": "https://clashofclans.fandom.com/wiki/Army_Camp/Home_Village",
        "Barracks": "https://clashofclans.fandom.com/wiki/Barracks/Home_Village",
        "Dark Barracks": "https://clashofclans.fandom.com/wiki/Dark_Barracks/Home_Village",
        "Laboratory": "https://clashofclans.fandom.com/wiki/Laboratory/Home_Village",
        "Spell Factory": "https://clashofclans.fandom.com/wiki/Spell_Factory/Home_Village",
        "Dark Spell Factory": "https://clashofclans.fandom.com/wiki/Dark_Spell_Factory/Home_Village",
        "Workshop": "https://clashofclans.fandom.com/wiki/Workshop/Home_Village",
        "Pet House": "https://clashofclans.fandom.com/wiki/Pet_House/Home_Village",
        "Blacksmith": "https://clashofclans.fandom.com/wiki/Blacksmith/Home_Village"
    },
    "troops": {
        "Barbarian": "https://clashofclans.fandom.com/wiki/Barbarian",
        "Archer": "https://clashofclans.fandom.com/wiki/Archer",
        "Giant": "https://clashofclans.fandom.com/wiki/Giant",
        "Goblin": "https://clashofclans.fandom.com/wiki/Goblin",
        "Wall Breaker": "https://clashofclans.fandom.com/wiki/Wall_Breaker",
        "Balloon": "https://clashofclans.fandom.com/wiki/Balloon",
        "Wizard": "https://clashofclans.fandom.com/wiki/Wizard",
        "Healer": "https://clashofclans.fandom.com/wiki/Healer",
        "Dragon": "https://clashofclans.fandom.com/wiki/Dragon",
        "P.E.K.K.A": "https://clashofclans.fandom.com/wiki/P.E.K.K.A",
        "Baby Dragon": "https://clashofclans.fandom.com/wiki/Baby_Dragon",
        "Miner": "https://clashofclans.fandom.com/wiki/Miner",
        "Electro Dragon": "https://clashofclans.fandom.com/wiki/Electro_Dragon",
        "Yeti": "https://clashofclans.fandom.com/wiki/Yeti",
        "Dragon Rider": "https://clashofclans.fandom.com/wiki/Dragon_Rider",
        "Electro Titan": "https://clashofclans.fandom.com/wiki/Electro_Titan",
        "Root Rider": "https://clashofclans.fandom.com/wiki/Root_Rider",
        "Minion": "https://clashofclans.fandom.com/wiki/Minion",
        "Hog Rider": "https://clashofclans.fandom.com/wiki/Hog_Rider",
        "Valkyrie": "https://clashofclans.fandom.com/wiki/Valkyrie",
        "Golem": "https://clashofclans.fandom.com/wiki/Golem",
        "Witch": "https://clashofclans.fandom.com/wiki/Witch",
        "Lava Hound": "https://clashofclans.fandom.com/wiki/Lava_Hound",
        "Bowler": "https://clashofclans.fandom.com/wiki/Bowler",
        "Ice Golem": "https://clashofclans.fandom.com/wiki/Ice_Golem",
        "Headhunter": "https://clashofclans.fandom.com/wiki/Headhunter",
        "Apprentice Warden": "https://clashofclans.fandom.com/wiki/Apprentice_Warden",
        "Druid": "https://clashofclans.fandom.com/wiki/Druid"
    },
    "traps": {
        "Bomb": "https://clashofclans.fandom.com/wiki/Bomb",
        "Spring Trap": "https://clashofclans.fandom.com/wiki/Spring_Trap",
        "Giant Bomb": "https://clashofclans.fandom.com/wiki/Giant_Bomb",
        "Air Bomb": "https://clashofclans.fandom.com/wiki/Air_Bomb",
        "Seeking Air Mine": "https://clashofclans.fandom.com/wiki/Seeking_Air_Mine",
        "Skeleton Trap": "https://clashofclans.fandom.com/wiki/Skeleton_Trap",
        "Tornado Trap": "https://clashofclans.fandom.com/wiki/Tornado_Trap"
    },
    "pets": {
        "L.A.S.S.I": "https://clashofclans.fandom.com/wiki/L.A.S.S.I",
        "Electro Owl": "https://clashofclans.fandom.com/wiki/Electro_Owl",
        "Mighty Yak": "https://clashofclans.fandom.com/wiki/Mighty_Yak",
        "Unicorn": "https://clashofclans.fandom.com/wiki/Unicorn",
        "Frosty": "https://clashofclans.fandom.com/wiki/Frosty",
        "Diggy": "https://clashofclans.fandom.com/wiki/Diggy",
        "Poison Lizard": "https://clashofclans.fandom.com/wiki/Poison_Lizard",
        "Phoenix": "https://clashofclans.fandom.com/wiki/Phoenix",
        "Spirit Fox": "https://clashofclans.fandom.com/wiki/Spirit_Fox",
        "Angry Jelly": "https://clashofclans.fandom.com/wiki/Angry_Jelly"
    },
    "heroes": {
        "Barbarian King": "https://clashofclans.fandom.com/wiki/Barbarian_King",
        "Archer Queen": "https://clashofclans.fandom.com/wiki/Archer_Queen",
        "Grand Warden": "https://clashofclans.fandom.com/wiki/Grand_Warden",
        "Royal Champion": "https://clashofclans.fandom.com/wiki/Royal_Champion",
        "Battle Machine": "https://clashofclans.fandom.com/wiki/Battle_Machine",
        "Battle Copter": "https://clashofclans.fandom.com/wiki/Battle_Copter"
    },
    "hero_equipment": {
        "Barbarian Puppet": "https://clashofclans.fandom.com/wiki/Barbarian_Puppet",
        "Rage Vial": "https://clashofclans.fandom.com/wiki/Rage_Vial",
        "Giant Gauntlet": "https://clashofclans.fandom.com/wiki/Giant_Gauntlet",
        "Earthquake Boots": "https://clashofclans.fandom.com/wiki/Earthquake_Boots",
        "Archer Puppet": "https://clashofclans.fandom.com/wiki/Archer_Puppet",
        "Invisibility Vial": "https://clashofclans.fandom.com/wiki/Invisibility_Vial",
        "Giant Arrow": "https://clashofclans.fandom.com/wiki/Giant_Arrow",
        "Healer Puppet": "https://clashofclans.fandom.com/wiki/Healer_Puppet",
        "Eternal Tome": "https://clashofclans.fandom.com/wiki/Eternal_Tome",
        "Life Gem": "https://clashofclans.fandom.com/wiki/Life_Gem",
        "Rage Gem": "https://clashofclans.fandom.com/wiki/Rage_Gem",
        "Healing Tome": "https://clashofclans.fandom.com/wiki/Healing_Tome"
    },
    "builder_base": {
        "Double Cannon": "https://clashofclans.fandom.com/wiki/Double_Cannon/Home_Village",
        "Crusher": "https://clashofclans.fandom.com/wiki/Crusher/Home_Village",
        "Roaster": "https://clashofclans.fandom.com/wiki/Roaster/Home_Village",
        "Giant Cannon": "https://clashofclans.fandom.com/wiki/Giant_Cannon/Home_Village",
        "Mega Tesla": "https://clashofclans.fandom.com/wiki/Mega_Tesla/Home_Village",
        "Lava Launcher": "https://clashofclans.fandom.com/wiki/Lava_Launcher/Home_Village",
        "Guard Post": "https://clashofclans.fandom.com/wiki/Guard_Post/Home_Village"
    },
    "builder_base_troops": {
        "Raged Barbarian": "https://clashofclans.fandom.com/wiki/Raged_Barbarian",
        "Sneaky Archer": "https://clashofclans.fandom.com/wiki/Sneaky_Archer",
        "Boxer Giant": "https://clashofclans.fandom.com/wiki/Boxer_Giant",
        "Beta Minion": "https://clashofclans.fandom.com/wiki/Beta_Minion",
        "Bomber": "https://clashofclans.fandom.com/wiki/Bomber",
        "Cannon Cart": "https://clashofclans.fandom.com/wiki/Cannon_Cart",
        "Night Witch": "https://clashofclans.fandom.com/wiki/Night_Witch",
        "Drop Ship": "https://clashofclans.fandom.com/wiki/Drop_Ship",
        "Power P.E.K.K.A": "https://clashofclans.fandom.com/wiki/Power_P.E.K.K.A",
        "Hog Glider": "https://clashofclans.fandom.com/wiki/Hog_Glider",
        "Electrofire Wizard": "https://clashofclans.fandom.com/wiki/Electrofire_Wizard"
    },
    "builder_base_traps": {
        "Push Trap": "https://clashofclans.fandom.com/wiki/Push_Trap",
        "Mine": "https://clashofclans.fandom.com/wiki/Mine/Builder_Base",
        "Mega Mine": "https://clashofclans.fandom.com/wiki/Mega_Mine/Builder_Base"
    }
}


def main():
    data = load_json(DATA_FILE)
    changes_log = load_json(CHANGES_FILE)
    all_changes = []

    for category, buildings_dict in CATEGORIES.items():
        if category not in data:
            data[category] = {}

        for building, url in buildings_dict.items():
            print(f"Updating {building} ({category})...")

            try:
                new_levels = scrape_defense(url)
                print(f"Found {len(new_levels)} levels for {building}")

                old_levels = data[category].get(building, {}).get("levels", {})
                changes = detect_changes(old_levels, new_levels, building)

                if changes:
                    print(f"{len(changes)} changes found in {building}")
                    all_changes.extend(changes)

                data[category][building] = {
                    "levels": new_levels
                }
            except Exception as e:
                print(f"Failed to update {building}: {e}")
                continue

    data["last_updated"] = datetime.now().isoformat()
    save_json(DATA_FILE, data)

    if all_changes:
        changes_log.setdefault("history", []).extend(all_changes)
        save_json(CHANGES_FILE, changes_log)

    print("Update completed.")


if __name__ == "__main__":
    main()