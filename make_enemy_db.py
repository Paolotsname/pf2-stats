import sqlite3
import csv
import json


# Function to execute SQL command on CSV data and save results to a JSON file
def execute_sql_on_csv(csv_file_path, json_file_path):
    # Step 1: Open the CSV file and read it
    with open(csv_file_path, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile)

        # Step 2: Connect to an in-memory SQLite database
        conn = sqlite3.connect(":memory:")  # or provide a file path for a persistent DB
        cursor = conn.cursor()

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
        for row in csvreader:
            # Ensure proper data types (convert to int or handle non-numeric cases)
            level = row["level"]
            hp = row.get("hp", "0").strip()
            ac = row.get("ac", "0").strip()
            fortitude = row.get("fortitude", "0").strip()
            reflex = row.get("reflex", "0").strip()
            will = row.get("will", "0").strip()

            # Attack bonus processing (sum of attacks)
            attack_bonus_list = row.get("attack_bonus", "").split()
            attack_bonus = sum(
                map(lambda x: int(x.strip(",+")), attack_bonus_list)
            ) / max(
                1, len(attack_bonus_list)
            )  # Avoid division by zero from "unseen servant"

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

        # Step 5: Modify the SQL query to ensure -1 comes before 0 and round averages to 2 decimal places
        sql_command_with_sorting = """
        SELECT
            level,
            ROUND(AVG(hp), 2) as avg_hp,
            ROUND(AVG(ac), 2) as avg_ac,
            ROUND(AVG(fortitude), 2) as avg_fort,
            ROUND(AVG(reflex), 2) as avg_refl,
            ROUND(AVG(will), 2) as avg_will,
            ROUND(AVG(attack_bonus), 2) as avg_attack_bonus,
            ROUND(AVG(CASE WHEN spell_dc != 0 THEN spell_dc END), 2) as avg_spell_dc,
            ROUND(AVG(CASE WHEN spell_attack_bonus != 0 THEN spell_attack_bonus END), 2) as avg_spell_attack_bonus
        FROM foo
        GROUP BY level
        ORDER BY CAST(level AS INTEGER) ASC;
        """

        # Step 6: Execute the SQL command with the adjusted sorting
        cursor.execute(sql_command_with_sorting)

        # Step 7: Fetch the result of the query
        results = cursor.fetchall()

        # Step 8: Save results to a JSON file
        with open(json_file_path, "w") as jsonfile:
            # Convert the results to a list of dictionaries
            column_names = [description[0] for description in cursor.description]
            results_dict = [dict(zip(column_names, row)) for row in results]

            # Write to JSON file
            json.dump(results_dict, jsonfile, indent=4)

        # Step 9: Close the database connection
        conn.close()


# Example usage
csv_file_path = "table-data.csv"  # Replace with your CSV file path
json_file_path = "results.json"  # Path to save the JSON file

# Execute the SQL query on the CSV data and save the result to a JSON file
execute_sql_on_csv(csv_file_path, json_file_path)
