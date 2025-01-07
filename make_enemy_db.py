import sqlite3
import csv
import json
import statistics


# Function to execute SQL command on CSV data and save results to a JSON file
def execute_sql_on_csv(csv_file_path, json_file_path):
    # Step 1: Open the CSV file and read it
    with open(csv_file_path, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile)

        # Collect all rows into a list (to be used later for attack values)
        data_rows = list(csvreader)

        # Step 2: Connect to an in-memory SQLite database
        conn = sqlite3.connect(":memory:")  # or provide a file path for a persistent DB
        cursor = conn.cursor()

        # Optional: Increase the memory cache to improve performance
        cursor.execute(
            "PRAGMA cache_size = 10000;"
        )  # Adjust cache size for better memory usage
        cursor.execute(
            "PRAGMA temp_store = MEMORY;"
        )  # Store temporary tables in memory

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
                spell_attack_bonus = (
                    int(spell_attack_bonus) if spell_attack_bonus else 0
                )
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

        # Step 5: Execute the SQL query for averages
        sql_command_avg = """
        SELECT
            level,
            ROUND(AVG(hp), 2) as hp,
            ROUND(AVG(ac), 2) as ac,
            ROUND(AVG(fortitude), 2) as fort,
            ROUND(AVG(reflex), 2) as refl,
            ROUND(AVG(will), 2) as will,
            null as attack_bonus,
            ROUND(AVG(CASE WHEN spell_dc != 0 THEN spell_dc END), 2) as spell_dc,
            ROUND(AVG(CASE WHEN spell_attack_bonus != 0 THEN spell_attack_bonus END), 2) as spell_attack_bonus
        FROM foo
        GROUP BY level
        ORDER BY CAST(level AS INTEGER) ASC;
        """
        cursor.execute(sql_command_avg)
        average_results = cursor.fetchall()

        # Step 6: Execute the SQL query for modes (Updated to exclude zeroes)
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
            null AS attack_bonus,
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

        # Step 7: Process attack_bonus values outside of SQL queries
        attack_values_avg = []
        attack_values_mode = []
        for row in data_rows:
            attacks_list = row[
                "attack_bonus"
            ].split()  # Ensure split for attack bonuses
            # Calculating average attack bonus for each level
            if attacks_list:
                attack_values_avg.append(
                    sum(map(lambda x: int(x.strip(",+")), attacks_list))
                    / len(attacks_list)
                )
                attack_values_mode.append(
                    statistics.mode([int(x.strip(",+")) for x in attacks_list])
                )
            else:
                attack_values_avg.append(0)
                attack_values_mode.append(0)

        # Step 8: Save results to a JSON file with the desired structure
        result_dict = []
        column_names = [description[0] for description in cursor.description]

        # Combine average and mode results into the JSON structure
        for i, (avg_row, mode_row) in enumerate(zip(average_results, mode_results)):
            level = avg_row[0]  # Fetch the level from average result
            average = dict(zip(column_names[1:], avg_row[1:]))  # Get averages from row
            mode = dict(zip(column_names[1:], mode_row[1:]))  # Get mode from row

            # Insert attack values into the JSON result
            average["attack_bonus"] = attack_values_avg[i]
            mode["attack_bonus"] = attack_values_mode[i]

            result_dict.append(
                {"level": level, "avg": average, "mode": mode}
            )  # Store 'avg' and 'mode' values at the same level

        # Step 9: Close the database connection
        conn.close()

        # Step 10: Write to JSON file
        with open(json_file_path, "w") as jsonfile:
            json.dump(result_dict, jsonfile, indent=4)


# Example usage
csv_file_path = "table-data.csv"  # Replace with your CSV file path
json_file_path = "results.json"  # Path to save the JSON file

# Execute the SQL query on the CSV data and save the result to a JSON file
execute_sql_on_csv(csv_file_path, json_file_path)
