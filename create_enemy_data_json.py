import sqlite3
import csv
import json
import statistics

csv_file_path = "table-data.csv"  # Replace with your CSV file path
json_file_path = "enemy_data.json"

with open(csv_file_path, newline="") as csvfile:
    csvreader = csv.DictReader(csvfile)

    # Collect all rows into a list (to be used later for attack values)
    data_rows = list(csvreader)

    # Step 2: Connect to an in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Optional: Increase the memory cache to improve performance
    cursor.execute(
        "PRAGMA cache_size = 10000;"
    )  # Adjust cache size for better memory usage
    cursor.execute("PRAGMA temp_store = MEMORY;")  # Store temporary tables in memory

    # Step 3: Create table schema in SQLite
    cursor.execute(
        """CREATE TABLE foo (
        level TEXT,
        hp INTEGER,
        ac INTEGER,
        fortitude INTEGER,
        reflex INTEGER,
        will INTEGER,
        attack_bonus INTEGER,
        spell_dc INTEGER,
        spell_attack_bonus INTEGER
    )"""
    )

    # Step 4: Insert data from CSV into SQLite with error handling
    for row in data_rows:
        level = row["level"]
        hp = row.get("hp", "0").strip()
        ac = row.get("ac", "0").strip()
        fortitude = row.get("fortitude", "0").strip()
        reflex = row.get("reflex", "0").strip()
        will = row.get("will", "0").strip()

        attack_bonus = None

        spell_dc = row.get("spell_dc", "0").strip()
        spell_attack_bonus = row.get("spell_attack_bonus", "0").strip()

        # Handle non-numeric values by converting them to integers or defaulting to 0
        try:
            ac = int(ac) if ac else 0
            fortitude = int(fortitude) if fortitude else 0
            reflex = int(reflex) if reflex else 0
            will = int(will) if will else 0
            spell_dc = int(spell_dc) if spell_dc else 0
            spell_attack_bonus = int(spell_attack_bonus) if spell_attack_bonus else 0
        except ValueError:
            ac = fortitude = reflex = will = spell_dc = spell_attack_bonus = 0

        cursor.execute(
            """INSERT INTO foo (level, hp, ac, fortitude, reflex, will, attack_bonus, spell_dc, spell_attack_bonus)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                level,
                hp,
                ac,
                fortitude,
                reflex,
                will,
                attack_bonus,
                spell_dc,
                spell_attack_bonus,
            ),
        )

    # Step 5: Means
    sql_command_avg = """
    SELECT
        level,
        ROUND(AVG(hp), 2) as hp,
        ROUND(AVG(ac), 2) as ac,
        ROUND(AVG(fortitude), 2) as fort,
        ROUND(AVG(reflex), 2) as refl,
        ROUND(AVG(will), 2) as will,
        NULL as attack_bonus,
        ROUND(AVG(CASE WHEN spell_dc != 0 THEN spell_dc END), 2) as spell_dc,
        ROUND(AVG(CASE WHEN spell_attack_bonus != 0 THEN spell_attack_bonus END), 2) as spell_attack_bonus
    FROM foo
    GROUP BY level
    ORDER BY CAST(level AS INTEGER) ASC;
    """
    cursor.execute(sql_command_avg)
    mean_results = cursor.fetchall()

    # Step 6: Modes (Excluding zeroes)
    sql_command_mode = """
    SELECT
        level,
        (
            SELECT hp
            FROM foo
            WHERE level = f.level AND hp != 0
            GROUP BY hp
            ORDER BY COUNT(hp) DESC
            LIMIT 1
        ) AS hp,
        (
            SELECT ac
            FROM foo
            WHERE level = f.level AND ac != 0
            GROUP BY ac
            ORDER BY COUNT(ac) DESC
            LIMIT 1
        ) AS ac,
        (
            SELECT fortitude
            FROM foo
            WHERE level = f.level AND fortitude != 0
            GROUP BY fortitude
            ORDER BY COUNT(fortitude) DESC
            LIMIT 1
        ) AS fort,
        (
            SELECT reflex
            FROM foo
            WHERE level = f.level AND reflex != 0
            GROUP BY reflex
            ORDER BY COUNT(reflex) DESC
            LIMIT 1
        ) AS refl,
        (
            SELECT will
            FROM foo
            WHERE level = f.level AND will != 0
            GROUP BY will
            ORDER BY COUNT(will) DESC
            LIMIT 1
        ) AS will,
        NULL AS attack_bonus,
        (
            SELECT spell_dc
            FROM foo
            WHERE level = f.level AND spell_dc != 0
            GROUP BY spell_dc
            ORDER BY COUNT(spell_dc) DESC
            LIMIT 1
        ) AS spell_dc,
        (
            SELECT spell_attack_bonus
            FROM foo
            WHERE level = f.level AND spell_attack_bonus != 0
            GROUP BY spell_attack_bonus
            ORDER BY COUNT(spell_attack_bonus) DESC
            LIMIT 1
        ) AS spell_attack_bonus
    FROM foo f
    GROUP BY level
    ORDER BY CAST(level AS INTEGER) ASC;
    """
    cursor.execute(sql_command_mode)
    mode_results = cursor.fetchall()

    # Step 8: Medians (TODO)
    sql_command_median = """
    SELECT
        level,
        NULL as hp,
        NULL as ac,
        NULL as fort,
        NULL as refl,
        NULL as will,
        NULL as attack_bonus,
        NULL as spell_dc,
        NULL as spell_attack_bonus
    FROM foo
    GROUP BY level
    ORDER BY CAST(level AS INTEGER) ASC;
    """
    cursor.execute(sql_command_median)
    median_results = cursor.fetchall()

    # Step 7: Process attack_bonus values outside of SQL queries
    attacks_per_level = [[] for _ in range(27)]
    attack_values_avg = []
    attack_values_mode = []
    attack_values_median = []

    for row in data_rows:
        # Split attack_bonus values by spaces or commas (ensure cleaning of any extraneous characters)
        attacks_list = [x.strip(",+ ") for x in row["attack_bonus"].split()]

        # Ensure the list contains valid integers (filtering out any non-numeric entries)
        valid_attacks = [int(x) for x in attacks_list if x.isdigit()]

        # Calculate averages attack bonus for each level
        if valid_attacks:
            level = int(row["level"]) + 1
            attacks_per_level[level].extend(valid_attacks)

    for i in range(27):
        attack_values_avg.append(
            round(sum(attacks_per_level[i]) / len(attacks_per_level[i]), 2)
        )
        attack_values_mode.append(statistics.mode(attacks_per_level[i]))
        attack_values_median.append(statistics.median(attacks_per_level[i]))

    # Step 8: Save results to a JSON file with the desired structure
    result_dict = []
    column_names = [description[0] for description in cursor.description]

    for i, (avg_row, mode_row, median_row) in enumerate(
        zip(mean_results, mode_results, median_results)
    ):
        level = avg_row[0]  # Fetch the level from averages result
        mean = dict(zip(column_names[1:], avg_row[1:]))
        median = dict(zip(column_names[1:], median_row[1:]))
        mode = dict(zip(column_names[1:], mode_row[1:]))

        # Insert attack values into the JSON result
        mean["attack_bonus"] = attack_values_avg[i]
        median["attack_bonus"] = attack_values_median[i]
        mode["attack_bonus"] = attack_values_mode[i]

        result_dict.append(
            {"level": level, "mean": mean, "median": median, "mode": mode}
        )

    # Step 9: Close the database connection
    conn.close()

    keys = list(result_dict[0].keys())
    inner_keys = list(result_dict[0]["mode"])
    for key in keys:
        if key != "level":
            result_dict[0][key + "_pwl"] = result_dict[0][key]
            result_dict[1][key + "_pwl"] = result_dict[1][key]
            for i in range(1, 26):
                result_dict[i + 1][key + "_pwl"] = dict()
                for inner_key in inner_keys:
                    if inner_key == "hp":
                        if result_dict[i + 1][key][inner_key] is not None:
                            result_dict[i + 1][key + "_pwl"][inner_key] = result_dict[
                                i + 1
                            ][key][inner_key]
                        else:
                            result_dict[i + 1][key + "_pwl"][inner_key] = None
                    if inner_key != "hp":
                        if result_dict[i + 1][key][inner_key] is not None:
                            result_dict[i + 1][key + "_pwl"][inner_key] = (
                                result_dict[i + 1][key][inner_key] - i
                            )
                        else:
                            result_dict[i + 1][key + "_pwl"][inner_key] = None

    # Step 10: Write to JSON file
    with open(json_file_path, "w") as jsonfile:
        json.dump(result_dict, jsonfile, indent=4)
