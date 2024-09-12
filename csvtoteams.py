import pandas as pd
import json

# Define the path to the CSV file
csv_file = "players_data1.csv"
df = pd.read_csv(csv_file)

# Function to evaluate division in a string
def evaluate_division(val):
    if isinstance(val, str) and '/' in val:
        try:
            return eval(val)
        except:
            return val
    return val

# Apply the function to the avg_min column
df['avg_min'] = df['avg_min'].apply(evaluate_division)

# Extract and rename relevant columns
df = df[['id', 'web_name', 'team', 'position', 'cost', 'minutes', 'saves_per_90', 'starts', 'expected_goals_per_90', 'expected_assists_per_90', 'expected_goals_conceded_per_90', 'avg_min']]
df.rename(columns={
    'expected_goals_per_90': 'xG90',
    'expected_assists_per_90': 'xA90',
    'expected_goals_conceded_per_90': 'xGC90'
}, inplace=True)

# Group by team
teams = df['team'].unique()
team_dict = {}

for team_id in teams:
    team_df = df[df['team'] == team_id]
    team_list = team_df.to_dict(orient='records')
    team_dict[team_id] = team_list  # No conversion to int needed

# Save the dictionary to a Python file with desired format
python_file = 'teams_data.py'
with open(python_file, 'w') as f:
    f.write('teams_data = {\n')
    for team_id, players in team_dict.items():
        f.write(f'    {team_id}: [\n')
        for player in players:
            f.write(f'        {json.dumps(player, separators=(",", ":"))},\n')
        f.write('    ],\n')
    f.write('}\n')

print(f"Teams data saved to {python_file}")