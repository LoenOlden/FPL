import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize
from updated_teams_data import teams_data

def calculate_avg_min2(starts, avg_min, minutes, position):
    if position == 1:  # Position 1 is for goalkeepers
        if minutes > 2700:
            return 89
        elif minutes > 1710:
            return 80
        elif minutes < 800:
            return 0
        else:
            return avg_min
    else:
        if starts == 0:
            return 0
        elif 1 <= starts <= 5:
            return 15
        elif 6 <= starts <= 29:
            return avg_min
        elif starts > 30 and minutes > 2700:
            return 90
        else:
            return avg_min

def process_team_data(teams_data):
    all_players = []
    
    for players in teams_data.values():
        for player in players:
            avg_min = player['avg_min']
            starts = player['starts']
            minutes = player['minutes']
            position = player['position']
            avg_min2 = calculate_avg_min2(starts, avg_min, minutes, position)
            
            player_data = player.copy()
            player_data['avg_min2'] = avg_min2
            player_data['avg_minutes'] = (avg_min + avg_min2) / 2
            
            all_players.append(player_data)
    
    return all_players

def predict_expected_minutes(players_df):
    # Ensure the columns used for training include 'avg_min2'
    X = players_df[['avg_min', 'avg_min2', 'minutes', 'starts']]
    y = players_df['avg_minutes']  # Use the average as the target variable
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict initial expected minutes
    players_df['initial_expected_minutes'] = model.predict(X)
    
    return players_df

def iterative_adjustment(players_df, iterations=4):
    adjusted_players = players_df.copy()
    
    for _ in range(iterations):
        adjusted_players = adjust_minutes(adjusted_players)
    
    return adjusted_players

def adjust_minutes(players_df):
    adjusted_players = []

    for team_id in players_df['team'].unique():
        team_players = players_df[players_df['team'] == team_id].copy()

        # Separate goalkeepers and other players
        goalkeepers = team_players[team_players['position'] == 1].copy()
        other_players = team_players[team_players['position'] != 1].copy()

        main_keepers = goalkeepers[goalkeepers['minutes'] >= 1710].copy()
        reserve_keepers = goalkeepers[goalkeepers['minutes'] < 1710].copy()

        # Separate players based on minutes
        main_players = other_players[other_players['minutes'] >= 1710].copy()
        reserve_players = other_players[other_players['minutes'] < 1710].copy()

        # Objective function for outfield players
        def objective_players(minutes):
            # Update 'expected_minutes' in the copied DataFrames
            main_players_copy = main_players.copy()
            reserve_players_copy = reserve_players.copy()
            
            main_players_copy['expected_minutes'] = minutes[:len(main_players)]
            reserve_players_copy['expected_minutes'] = minutes[len(main_players):]
            
            # Calculate the mean squared error for outfield players
            mse_penalty = ((main_players_copy['avg_minutes'] - main_players_copy['expected_minutes']) ** 2).sum()
            
            return mse_penalty

        # Constraint for outfield players
        def constraint_players(minutes):
            return 900 - minutes.sum()

        # Objective function for goalkeepers
        def objective_keepers(minutes):
            # Update 'expected_minutes' in the copied DataFrames
            main_keepers_copy = main_keepers.copy()
            reserve_keepers_copy = reserve_keepers.copy()
            
            main_keepers_copy['expected_minutes'] = minutes[:len(main_keepers)]
            reserve_keepers_copy['expected_minutes'] = minutes[len(main_keepers):]
            
            # Calculate the mean squared error for goalkeepers
            mse_penalty = ((main_keepers_copy['avg_minutes'] - main_keepers_copy['expected_minutes']) ** 2).sum()
            
            return mse_penalty

        # Constraint for goalkeepers
        def constraint_keepers(minutes):
            return 90 - minutes.sum()

        # Optimization for outfield players
        cons_players = {'type': 'eq', 'fun': constraint_players}
        bounds_players = [(0, 90)] * (len(main_players) + len(reserve_players))
        initial_guess_players = main_players['initial_expected_minutes'].tolist() + reserve_players['initial_expected_minutes'].tolist()

        result_players = minimize(objective_players, initial_guess_players, bounds=bounds_players, constraints=cons_players)

        if result_players.success:
            main_players['expected_minutes'] = result_players.x[:len(main_players)]
            reserve_players['expected_minutes'] = result_players.x[len(main_players):]
        else:
            # If optimization fails, retain the initial expected minutes
            main_players['expected_minutes'] = main_players['initial_expected_minutes']
            reserve_players['expected_minutes'] = reserve_players['initial_expected_minutes']

        # Optimization for goalkeepers
        cons_keepers = {'type': 'eq', 'fun': constraint_keepers}
        bounds_keepers = [(0, 90)] * (len(main_keepers) + len(reserve_keepers))
        initial_guess_keepers = main_keepers['initial_expected_minutes'].tolist() + reserve_keepers['initial_expected_minutes'].tolist()

        result_keepers = minimize(objective_keepers, initial_guess_keepers, bounds=bounds_keepers, constraints=cons_keepers)

        if result_keepers.success:
            main_keepers['expected_minutes'] = result_keepers.x[:len(main_keepers)]
            reserve_keepers['expected_minutes'] = result_keepers.x[len(main_keepers):]
        else:
            # If optimization fails, retain the initial expected minutes
            main_keepers['expected_minutes'] = main_keepers['initial_expected_minutes']
            reserve_keepers['expected_minutes'] = reserve_keepers['initial_expected_minutes']

        # Combine results
        adjusted_team_players = pd.concat([main_keepers, reserve_keepers, main_players, reserve_players])
        adjusted_players.append(adjusted_team_players)

    return pd.concat(adjusted_players)

def format_player_data(player):
    return (f'{{"id": {player["id"]}, "web_name": "{player["web_name"]}", "team": {player["team"]}, '
            f'"position": {player["position"]}, "cost": {player["cost"]}, "minutes": {player["minutes"]}, '
            f'"saves_per_90": {player["saves_per_90"]}, "starts": {player["starts"]}, '
            f'"xG90": {player["xG90"]}, "xA90": {player["xA90"]}, "xGC90": {player["xGC90"]}, '
            f'"avg_min": {player["avg_min"]}, "csP": {player["csP"]}, "xcg23": {player["xcg23"]}, '
            f'"xcg45": {player["xcg45"]}, "3shots": {player["3shots"]}, "6shots": {player["6shots"]}, '
            f'"expected_minutes": {player["expected_minutes"]:.2f}}},')

def main():
    all_players = process_team_data(teams_data)
    players_df = pd.DataFrame(all_players)
    players_df = predict_expected_minutes(players_df)
    players_df = iterative_adjustment(players_df, iterations=4)
    
    with open("updated_player_data.py", "w", encoding="utf-8") as f:
        f.write("players_data = [\n")
        for player in players_df.to_dict(orient='records'):
            player_str = format_player_data(player)
            f.write(player_str + "\n")
        f.write("]\n")
    
    print("Updated player data with expected minutes has been saved.")

if __name__ == "__main__":
    main()