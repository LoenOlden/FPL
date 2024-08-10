import csv
import os
import json
from collections import defaultdict

# Team mappings
team_mappings = {
    1: ('ARS', 'Arsenal'),
    2: ('AVL', 'Aston Villa'),
    3: ('BOU', 'Bournemouth'),
    4: ('BRE', 'Brentford'),
    5: ('BHA', 'Brighton'),
    6: ('CHE', 'Chelsea'),
    7: ('CRY', 'Crystal Palace'),
    8: ('EVE', 'Everton'),
    9: ('FUL', 'Fulham'),
    10: ('IPS', 'Ipswich'),
    11: ('LEI', 'Leicester'),
    12: ('LIV', 'Liverpool'),
    13: ('MCI', 'Man City'),
    14: ('MUN', 'Man Utd'),
    15: ('NEW', 'Newcastle'),
    16: ('NFO', 'Nott\'m Forest'),
    17: ('SOU', 'Southampton'),
    18: ('TOT', 'Spurs'),
    19: ('WHU', 'West Ham'),
    20: ('WOL', 'Wolves')
}

# Initialize dictionary to hold players by team
players_by_team = defaultdict(list)

# Path to your CSV file
csv_file_path = "players_data.csv"

# Check if the file exists
if not os.path.isfile(csv_file_path):
    print(f"File not found: {csv_file_path}")
    print("Current working directory:", os.getcwd())
    exit(1)

# Read and process the CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)  # Read the header row
    
    for row in csvreader:
        team_id = int(row[4])  # Assuming 'team' is the fifth column
        short_name, long_name = team_mappings[team_id]
        players_by_team[long_name].append(row)

# Convert the defaultdict to a regular dictionary for JSON serialization
players_by_team = dict(players_by_team)

# Path to save the JSON file
json_file_path = "players_by_team.json"

# Write the grouped players to a JSON file
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(players_by_team, jsonfile, ensure_ascii=False, indent=4)

print(f"Data successfully saved to {json_file_path}")