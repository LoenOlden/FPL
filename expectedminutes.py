import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize
from updated_teams_data import teams_data

def process_team_data(teams_data):
    all_players = []
    
    for players in teams_data.values():
        for player in players:
            # Use available data only
            player_data = {
                "id": player["id"],
                "web_name": player["web_name"],
                "team": player["team"],
                "position": player["position"],
                "cost": player["cost"],
                "minutes": player["minutes"],
                "saves_per_90": player["saves_per_90"],
                "xG90": player["xG90"],
                "xA90": player["xA90"],
                "xGC90": player["xGC90"],
                "csP": player["csP"],
                "xcg23": player["xcg23"],
                "xcg45": player["xcg45"],
                "3shots": player["3shots"],
                "6shots": player["6shots"],
            }
            all_players.append(player_data)
    
    return all_players

def predict_expected_minutes(players_df):
    # Use available features for prediction
    X = players_df[['minutes', 'position', 'xG90', 'xA90', 'xGC90', 'csP', 'xcg23', 'xcg45', '3shots', '6shots']]
    y = players_df['minutes']  # Use 'minutes' as the target variable, as it's the closest thing we have to the past average

    model = LinearRegression()
    model.fit(X, y)
    
    # Predict initial expected minutes, ensuring they sum to a reasonable amount
    players_df['initial_expected_minutes'] = model.predict(X)
    
    # Normalize the predicted minutes to 900 for each team
    players_df['initial_expected_minutes'] = players_df.groupby('team')['initial_expected_minutes'].transform(
        lambda x: 900 * (x / x.sum())
    )
    
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

        main_players = other_players[other_players['minutes'] >= 1710].copy()
        reserve_players = other_players[other_players['minutes'] < 1710].copy()

        # Objective function for outfield players
        def objective_players(minutes):
            main_players_copy = main_players.copy()
            reserve_players_copy = reserve_players.copy()
            
            main_players_copy['expected_minutes'] = minutes[:len(main_players)]
            reserve_players_copy['expected_minutes'] = minutes[len(main_players):]
            
            mse_penalty = ((main_players_copy['minutes'] - main_players_copy['expected_minutes']) ** 2).sum()
            
            return mse_penalty

        # Constraint for outfield players
        def constraint_players(minutes):
            return 900 - minutes.sum()

        # Objective function for goalkeepers
        def objective_keepers(minutes):
            main_keepers_copy = main_keepers.copy()
            reserve_keepers_copy = reserve_keepers.copy()
            
            main_keepers_copy['expected_minutes'] = minutes[:len(main_keepers)]
            reserve_keepers_copy['expected_minutes'] = minutes[len(main_keepers):]
            
            mse_penalty = ((main_keepers_copy['minutes'] - main_keepers_copy['expected_minutes']) ** 2).sum()
            
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
            main_keepers['expected_minutes'] = main_keepers['initial_expected_minutes']
            reserve_keepers['expected_minutes'] = reserve_keepers['initial_expected_minutes']

        adjusted_team_players = pd.concat([main_keepers, reserve_keepers, main_players, reserve_players])
        adjusted_players.append(adjusted_team_players)

    return pd.concat(adjusted_players)

def format_player_data(player):
    return (f'{{"id": {player["id"]}, "web_name": "{player["web_name"]}", "team": {player["team"]}, '
            f'"position": {player["position"]}, "cost": {player["cost"]}, "minutes": {player["minutes"]}, '
            f'"saves_per_90": {player["saves_per_90"]}, "xG90": {player["xG90"]}, "xA90": {player["xA90"]}, '
            f'"xGC90": {player["xGC90"]}, "csP": {player["csP"]}, "xcg23": {player["xcg23"]}, '
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
