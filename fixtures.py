import requests
import csv
from datetime import datetime

# URLs
fixtures_url = "https://fantasy.premierleague.com/api/fixtures/"
bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Get data
fixtures_response = requests.get(fixtures_url, headers=headers)
bootstrap_response = requests.get(bootstrap_url, headers=headers)

if fixtures_response.status_code != 200 or bootstrap_response.status_code != 200:
    print("Failed to fetch data")
    print("Fixtures:", fixtures_response.status_code)
    print("Bootstrap:", bootstrap_response.status_code)
    exit()

# Parse JSON
fixtures = fixtures_response.json()
teams = bootstrap_response.json()["teams"]

# Map team ID to name
team_id_to_name = {team['id']: team['name'] for team in teams}

# Write to CSV
with open('fixtures.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Gameweek", "Home Team", "Away Team", "Kickoff", "Probability"])

    for fixture in fixtures:
        if fixture['kickoff_time'] is None:
            continue

        gw = f"GW{fixture['event']}"
        home_team = team_id_to_name[fixture['team_h']]
        away_team = team_id_to_name[fixture['team_a']]
        kickoff = datetime.fromisoformat(fixture['kickoff_time'].replace("Z", "")).strftime('%Y-%m-%d %H:%M:%S')
        probability = 1.00  # Placeholder

        writer.writerow([gw, home_team, away_team, kickoff, f"{probability:.2f}"])