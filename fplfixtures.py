from datetime import datetime
from collections import defaultdict
import csv

def parse_fixtures(raw_data):
    fixtures = defaultdict(list)
    lines = raw_data.splitlines()
    
    # Process only the first 190 lines
    lines = lines[:190]
    
    # Divide the lines into groups of 10 for each gameweek
    for i, line in enumerate(lines):
        gameweek = (i // 10) + 1
        parts = line.split(" - Kickoff: ")
        if len(parts) == 2:
            teams, kickoff_str = parts
            kickoff = datetime.strptime(kickoff_str, '%Y-%m-%dT%H:%M:%SZ')
            team2, team1 = teams.split(' vs ')
            fixtures[f"GW{gameweek}"].append({
                'team1': team1.strip(),
                'team2': team2.strip(),
                'kickoff': kickoff
            })
    
    # Sort fixtures within each gameweek by kickoff time
    for gameweek in fixtures:
        fixtures[gameweek].sort(key=lambda x: x['kickoff'])
    
    return fixtures

def print_fixtures(fixtures):
    for gameweek, matches in fixtures.items():
        print(f"{gameweek}:")
        for match in matches:
            print(f"  {match['team1']} vs {match['team2']} - Kickoff: {match['kickoff']}")
        print()  # Add a blank line between gameweeks

def export_to_csv(fixtures, filename='fixtures.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Gameweek', 'Home Team', 'Away Team', 'Kickoff'])
        
        for gameweek, matches in fixtures.items():
            for match in matches:
                writer.writerow([gameweek, match['team1'], match['team2'], match['kickoff'].strftime('%Y-%m-%d %H:%M:%S')])

if __name__ == "__main__":
    # Replace this with the path to your raw data file
    with open('fixtures.txt', 'r') as file:
        raw_data = file.read()
    
    fixtures = parse_fixtures(raw_data)
    print_fixtures(fixtures)
    export_to_csv(fixtures)