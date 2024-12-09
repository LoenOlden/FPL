import pandas as pd

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

# Group by position
positions = sorted(df['position'].unique())
position_dict = {}

for position_id in positions:
    position_df = df[df['position'] == position_id]
    position_list = position_df.to_dict(orient='records')
    position_dict[position_id] = position_list

python_file = 'positions_data.py'
with open(python_file, 'w', encoding='utf-8') as f:
    f.write('positions_data = {\n')
    for position_id in positions:
        f.write(f'    {position_id}: [\n')
        for player in position_dict[position_id]:
            f.write(f'        {player},\n')
        f.write('    ],\n')
    f.write('}\n')

print(f"Positions data saved to {python_file}")
