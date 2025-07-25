from updated_player_data import players_data
        
for player in players_data:
    if player['cost'] > 5.3 and player['position'] != 1 and player['xG90'] == 0.0 and player['xA90'] == 0.0:
        print(f"Player: {player['web_name']}, xG90: {player['xG90']}, xA90: {player['xA90']}")

for player in players_data:
    if player['position'] == 2 and player['CBIT90'] == 0.0 and player['CBITR90'] > 0.0:
        print(f"Player: {player['web_name']}, xG90: {player['xG90']}, xA90: {player['xA90']}")
        
for player in players_data:
    if player['position'] == 3 and player['CBIT90'] > 0.0 and player['CBITR90'] == 0.0:
        print(f"Player: {player['web_name']}, xG90: {player['xG90']}, xA90: {player['xA90']}")
        
for player in players_data:
    if player['position'] == 4 and player['CBIT90'] > 0.0 and player['CBITR90'] == 0.0:
        print(f"Player: {player['web_name']}, xG90: {player['xG90']}, xA90: {player['xA90']}")
        
for player in players_data:
    if (player['xG90'] > 0.0 or player['xA90'] > 0.0) and player['CBIT90'] == 0.0:
        print(f"Player: {player['web_name']}, xG90: {player['xG90']}, xA90: {player['xA90']}")
        
for player in players_data:
    if player['position'] == 4 and player['CBIT90'] > 0.0 and player['CBITR90'] == 0.0:
        print(f"Player: {player['web_name']}, xG90: {player['xG90']}, xA90: {player['xA90']}")
        
for player in players_data:
    if player['position'] != 1 and player['expected_minutes'] > 20.0 and player['CBIT90'] == 0.0:
        print(f"Player: {player['web_name']}, xG90: {player['xG90']}, xA90: {player['xA90']}")
        
for player in players_data:
    if player['CBIT90'] > 10.0:
        print(f"Player: {player['web_name']}")
        