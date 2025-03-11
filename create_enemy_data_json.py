import json
import csv
import re
from enum import Enum
import statistics


class Stats(Enum):
    hp = 0
    ac = 1
    fort = 2
    reflex = 3
    will = 4
    attack_bonus = 5
    spell_dc = 6
    spell_attack_bonus = 7


csv_file_path = "table-data.csv"
json_file_path = "enemy_data.json"
db = [[[] for _ in range(len(Stats))] for _ in range(27)]

with open(csv_file_path, newline="") as csvfile:
    csvreader = csv.DictReader(csvfile)

    # Collect all rows into a list (to be used later for attack values)
    data_rows = list(csvreader)
    for row in data_rows:
        level = int(row["level"])
        db[level + 1][Stats.hp.value].append(int(re.search(r"\d+", row["hp"]).group()))
        db[level + 1][Stats.ac.value].append(int(re.search(r"\d+", row["ac"]).group()))
        db[level + 1][Stats.fort.value].append(
            int(re.search(r"\d+", row["fortitude"]).group())
        )
        db[level + 1][Stats.reflex.value].append(
            int(re.search(r"\d+", row["reflex"]).group())
        )
        db[level + 1][Stats.will.value].append(
            int(re.search(r"\d+", row["will"]).group())
        )

        db[level + 1][Stats.attack_bonus.value].extend(
            int(match) for match in re.findall(r"\d+", row["attack_bonus"])
        )

        if len(row["spell_dc"]) > 0:
            db[level + 1][Stats.spell_dc.value].append(
                int(re.search(r"\d+", row["spell_dc"]).group())
            )

        if len(row["spell_attack_bonus"]) > 0:
            db[level + 1][Stats.spell_attack_bonus.value].append(
                int(re.search(r"\d+", row["spell_attack_bonus"]).group())
            )

    final_json = {}
    for level in range(27):
        final_json[str(level - 1)] = {
            "mean": {},
            "median": {},
            "mode": {},
            "mean_pwl": {},
            "median_pwl": {},
            "mode_pwl": {},
        }
        for avg, function in [
            ("mean", statistics.mean),
            ("median", statistics.median),
            ("mode", statistics.mode),
        ]:
            for stat in Stats:
                try:
                    final_json[str(level - 1)][avg][stat.name] = round(
                        function(db[level][stat.value]), 3
                    )
                # no creatures with spell_dc or spell_attack_bonus on level
                except statistics.StatisticsError:
                    final_json[str(level - 1)][avg][stat.name] = 0
                finally:
                    final_json[str(level - 1)][f"{avg}_pwl"][stat.name] = final_json[
                        str(level - 1)
                    ][avg][stat.name] - (level if level > 0 else 0)

    with open(json_file_path, "w") as jsonfile:
        json.dump(final_json, jsonfile, indent=4)
