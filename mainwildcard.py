import pulp
import pandas as pd
from final_player_data import player_gameweek_data

HIT_VALUE = 4.0
budget = 100.0
bench_budget = 0.0
num_weeks = 8
decay_rate = 0.99
start_week = 1
max_transfers = 0

banned_players = ["Füllkrug", "R.Gomes", "Munetsi", "Doherty", "Raúl", "Wood", "Cash", "Mayenda"]
locked_players = ["Kelleher", "José Sá", "Palmer"]

def load_player_data():
    # Convert player_gameweek_data to DataFrame
    gameweek_data = []
    for player in player_gameweek_data:
        if player["name"] in banned_players:
            continue
        if player['GW1'] < 0.8:
            continue
        scores = {gw: float(score) for gw, score in player.items() if gw.startswith('GW')}
        gameweek_data.append({
            'id': player["id"],
            'name': player["name"],
            'position': player["position"],
            'team': player["team"],
            'price': float(player["price"]),
            **scores
        })
    players_df = pd.DataFrame(gameweek_data)
    return players_df

def apply_decay_factors(players, decay_factors):
    # Apply decay factors to players' expected points
    for gw in players.columns:
        if gw.startswith('GW'):
            week = int(gw[2:])
            # Apply decay factor for each week
            if week in decay_factors:
                players[gw] = players[gw] * decay_factors[week]

def create_optimization_problem(players, budget, bench_budget, decay_factors, num_weeks, start_week, locked_players):
    prob = pulp.LpProblem("FantasyFootballTeamSelection", pulp.LpMaximize)
    # Decision variables
    x_selected = pulp.LpVariable.dicts("x_selected", (players.index, range(start_week, start_week + num_weeks)), cat='Binary')
    x_main = pulp.LpVariable.dicts("x_main", (players.index, range(start_week, start_week + num_weeks)), cat='Binary')
    x_bench = pulp.LpVariable.dicts("x_bench", (players.index, range(start_week, start_week + num_weeks)), cat='Binary')
    x_transfer_in = pulp.LpVariable.dicts("x_transfer_in", (players.index, range(start_week + 1, start_week + num_weeks)), cat='Binary')
    x_transfer_out = pulp.LpVariable.dicts("x_transfer_out", (players.index, range(start_week + 1, start_week + num_weeks)), cat='Binary')
    x_captain = pulp.LpVariable.dicts("x_captain", (players.index, range(start_week, start_week + num_weeks)), cat='Binary')

    # Add constraints for locked players
    locked_indices = players[players['name'].isin(locked_players)].index
    for week in range(start_week, start_week + num_weeks):
        for i in locked_indices:
            prob += x_selected[i][week] == 1, f"Locked_player_{i}_week_{week}"

    # Constraints for each week
    for week in range(start_week, start_week + num_weeks):
        week_index = week - start_week
        prob += pulp.lpSum(x_selected[i][week] for i in players.index) == 15, f"Total_players_week_{week}"
        prob += pulp.lpSum(x_selected[i][week] for i in players.index if players.loc[i, 'position'] == 1) == 2, f"GK_week_{week}"
        prob += pulp.lpSum(x_selected[i][week] for i in players.index if players.loc[i, 'position'] == 2) == 5, f"DEF_week_{week}"
        prob += pulp.lpSum(x_selected[i][week] for i in players.index if players.loc[i, 'position'] == 3) == 5, f"MID_week_{week}"
        prob += pulp.lpSum(x_selected[i][week] for i in players.index if players.loc[i, 'position'] == 4) == 3, f"FWD_week_{week}"

        prob += pulp.lpSum(x_main[i][week] for i in players.index) == 11, f"Main_players_week_{week}"
        prob += pulp.lpSum(x_bench[i][week] for i in players.index) == 4, f"Bench_players_week_{week}"

        prob += pulp.lpSum(x_main[i][week] for i in players.index if players.loc[i, 'position'] == 1) == 1, f"Main_GK_week_{week}"
        prob += pulp.lpSum(x_main[i][week] for i in players.index if players.loc[i, 'position'] == 2) >= 3, f"Min_DEF_week_{week}"
        prob += pulp.lpSum(x_main[i][week] for i in players.index if players.loc[i, 'position'] == 2) <= 5, f"Max_DEF_week_{week}"
        prob += pulp.lpSum(x_main[i][week] for i in players.index if players.loc[i, 'position'] == 3) >= 2, f"Min_MID_week_{week}"
        prob += pulp.lpSum(x_main[i][week] for i in players.index if players.loc[i, 'position'] == 3) <= 5, f"Max_MID_week_{week}"
        prob += pulp.lpSum(x_main[i][week] for i in players.index if players.loc[i, 'position'] == 4) >= 1, f"Min_FWD_week_{week}"
        prob += pulp.lpSum(x_main[i][week] for i in players.index if players.loc[i, 'position'] == 4) <= 3, f"Max_FWD_week_{week}"

        for i in players.index:
            prob += x_main[i][week] + x_bench[i][week] == x_selected[i][week], f"Main_or_bench_{i}_week_{week}"

        teams = players['team'].unique()
        for team in teams:
            prob += pulp.lpSum(x_selected[i][week] for i in players.index if players.loc[i, 'team'] == team) <= 3, f"Max_players_from_{team}_week_{week}"

        prob += pulp.lpSum(players.loc[i, 'price'] * x_selected[i][week] for i in players.index) <= budget, f"Budget_week_{week}"
        prob += pulp.lpSum(players.loc[i, 'price'] * x_bench[i][week] for i in players.index) >= bench_budget, f"Bench_Budget_week_{week}"

        # Ensure only one captain is selected per week
        prob += pulp.lpSum(x_captain[i][week] for i in players.index) == 1, f"One_captain_week_{week}"

        for i in players.index:
            # Ensure only main players can be captains
            prob += x_captain[i][week] <= x_main[i][week], f"Captain_main_player_{i}_week_{week}"

    for week in range(start_week + 1, start_week + num_weeks):
        prob += pulp.lpSum(x_transfer_in[i][week] for i in players.index) <= max_transfers, f"Max_transfers_in_week_{week}"
        prob += pulp.lpSum(x_transfer_out[i][week] for i in players.index) <= max_transfers, f"Max_transfers_out_week_{week}"

        for i in players.index:
            prob += x_selected[i][week] == x_selected[i][week-1] + x_transfer_in[i][week] - x_transfer_out[i][week], f"Transfer_balance_{i}_week_{week}"

    # Objective function
    total_points = pulp.lpSum(players.loc[i, f'GW{week}'] * (x_main[i][week] + x_captain[i][week]) for week in range(start_week, start_week + num_weeks) for i in players.index)
    transfer_penalty = HIT_VALUE * pulp.lpSum(x_transfer_in[i][week] for week in range(start_week + 1, start_week + num_weeks) for i in players.index)

    objective_function = total_points - transfer_penalty
    prob += objective_function, "Maximize_Effective_Value"

    return prob, x_selected, x_main, x_bench, x_transfer_in, x_transfer_out, x_captain

def optimize_team(players, budget, bench_budget, num_weeks, decay_rate, start_week, locked_players):
    # Determine the gameweeks dynamically
    gameweeks = [col for col in players.columns if col.startswith('GW') and int(col[2:]) >= start_week][:num_weeks]

    # Compute decay factors for each gameweek starting from start_week
    decay_factors = {int(gw[2:]): decay_rate ** (idx) for idx, gw in enumerate(gameweeks)}

    # Ensure the first gameweek does not have decay
    decay_factors[start_week] = 1.0

    # Apply decay factors to players' expected points
    apply_decay_factors(players, decay_factors)

    # Create optimization problem
    prob, x_selected, x_main, x_bench, x_transfer_in, x_transfer_out, x_captain = create_optimization_problem(players, budget, bench_budget, decay_factors, num_weeks, start_week, locked_players)

    # Solve the problem
    prob.solve()

    # Check solver status
    if pulp.LpStatus[prob.status] != 'Optimal':
        print("Solver Status:", pulp.LpStatus[prob.status])
        for constraint in prob.constraints.values():
            print(f"Constraint {constraint.name}: {constraint.value()}")
        raise Exception("No optimal solution found. Check the constraints and budget limits.")

    # Extract the selected players for each week
    selected_players = {week: [i for i in players.index if x_selected[i][week].varValue == 1] for week in range(start_week, start_week + num_weeks)}
    selected_main_players = {week: [i for i in players.index if x_main[i][week].varValue == 1] for week in range(start_week, start_week + num_weeks)}
    selected_bench_players = {week: [i for i in players.index if x_bench[i][week].varValue == 1] for week in range(start_week, start_week + num_weeks)}
    selected_captains = {week: [i for i in players.index if x_captain[i][week].varValue == 1][0] for week in range(start_week, start_week + num_weeks)}

    # Get the transfers for each week
    transfers = {week: {'in': [i for i in players.index if x_transfer_in[i][week].varValue == 1],
                        'out': [i for i in players.index if x_transfer_out[i][week].varValue == 1]}
                 for week in range(start_week + 1, start_week + num_weeks)}

    return selected_main_players, selected_bench_players, selected_captains, transfers

def display_team(players, selected_main_players, selected_bench_players, selected_captains):
    for week, main_players in selected_main_players.items():
        print(f"\nGameweek {week}:")
        gw_column = f'GW{week}'

        main_players_df = players.loc[main_players]
        bench_players_df = players.loc[selected_bench_players[week]]

        total_value = main_players_df['price'].sum() + bench_players_df['price'].sum()
        print(f"Total team value: {total_value:.1f}")

        # Sort by position ascending, then GW points descending
        main_players_sorted = main_players_df.sort_values(by=['position', gw_column], ascending=[True, False])
        bench_players_sorted = bench_players_df.sort_values(by=['position', gw_column], ascending=[True, False])

        print("Main players:")
        print(main_players_sorted[['name', 'position', 'team', 'price', gw_column]])

        print("\nBench players:")
        print(bench_players_sorted[['name', 'position', 'team', 'price', gw_column]])

        captain_name = players.loc[selected_captains[week], 'name']
        print(f"\nCaptain: {captain_name}")

# Load player data
players_df = load_player_data()

# Optimize the team
selected_main_players, selected_bench_players, selected_captains, transfers = optimize_team(
    players_df, budget, bench_budget, num_weeks, decay_rate, start_week, locked_players
)

# Display the selected players with names and their scores for each gameweek
display_team(players_df, selected_main_players, selected_bench_players, selected_captains)

# Display transfers
for week, transfer in transfers.items():
    print(f"\nTransfers for week {week}:")
    if transfer['in'] or transfer['out']:
        print("In:", [players_df.loc[i, 'name'] for i in transfer['in']])
        print("Out:", [players_df.loc[i, 'name'] for i in transfer['out']])
    else:
        print("No transfers made this week.")
